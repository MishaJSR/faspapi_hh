import copy
from pathlib import Path
from abc import ABC, abstractmethod

import torch
from torch import nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
import pandas as pd
from loguru import logger

from tqdm import tqdm

MODELS_FOLDER = Path(__file__).parent.joinpath("models")


# Общий класс для классификации по произвольным меткам групп
class AbstractClassificator(ABC):
    def __init__(self, classes: list, model: [...], tokenizer: [...]):
        self.device = "cpu" if torch.cuda.is_available() else "cpu"
        self.model = model.to(self.device)
        self.tokenizer = tokenizer
        self.classes = classes

    # Установление других ортобазисных векторов (задача рефералов)
    def setClasses(self, classes: list):
        self.classes = classes

    # Расчет отнесения классов согласно уровню доверия
    def alphaProbabilityBorder(self, probabilities: list, alpha: float = 0.7, **kwargs):
        classes = kwargs.get("classes", self.classes)
        result = []
        for probability in probabilities:
            result.append([classes[y] for y in [list(probability).index(x) for x in probability if x >= alpha]])
        return result

    # Предсказание для любых классов
    @abstractmethod
    def predict(self, *args, **kwargs):
        pass

    # Вывод pandas-таблицы, матрицы вероятностей класс-объект, softmax-вывод принадлежности к классу
    def __call__(self, texts: list, pandas: bool = True, softmax: bool = False, **kwargs):
        normalize = kwargs.get("normalize", False)

        total_probs = []
        for text in tqdm(texts, desc="Classifyer predictions in progress:"):
            total_probs.append(self.predict(text, **kwargs))

        if pandas:
            logger.info("Softmax param has no aplication since pandas=True is set") if softmax else logger.info(
                "Pandas table processing")
            return pd.DataFrame(data=total_probs, index=texts, columns=self.classes)
        else:
            classes_view = [self.classes[torch.argmax(torch.Tensor(x)).item()] for x in total_probs]
            return classes_view if softmax else total_probs


# Оценка принадлежности по ZeroShot (finetune-rubert)
class ZeroShotClassisficator(AbstractClassificator):
    def __init__(self, classes: list):
        model = AutoModelForSequenceClassification.from_pretrained(MODELS_FOLDER.joinpath("rubert-base").__str__())
        tokenizer = AutoTokenizer.from_pretrained(MODELS_FOLDER.joinpath("rubert-base").__str__())
        super().__init__(classes=classes, model=model, tokenizer=tokenizer)

    def predict(self, text: str, **kwargs):
        normalize = kwargs.get("normalize")
        label = 'entailment'
        tokens = self.tokenizer([text] * len(self.classes), self.classes, truncation=True, return_tensors='pt',
                                padding=True)
        with torch.inference_mode():
            result = torch.softmax(self.model(**tokens.to(self.model.device)).logits, -1)
        proba = result[:, self.model.config.label2id[label]].cpu().numpy()
        if normalize:
            proba /= sum(proba)

        tokens.to("cpu")
        result.to("cpu")
        del tokens
        del result
        return proba


# Оценка принадлежности по DeepPavlov (rubert)
class DeepPavlovClassificator(AbstractClassificator):
    def __init__(self, classes):
        model = AutoModel.from_pretrained(MODELS_FOLDER.joinpath("deep-pavlov-rubert").__str__())
        tokenizer = AutoTokenizer.from_pretrained(MODELS_FOLDER.joinpath("deep-pavlov-rubert").__str__())
        super().__init__(classes=classes, model=model, tokenizer=tokenizer)

    def predict(self, text: str, **kwargs):
        cosine = nn.CosineSimilarity(-1)
        input_sequence = copy.copy(self.classes)
        input_sequence.append(text)

        tokenized_input = self.tokenizer(input_sequence, padding=True, return_tensors='pt').to(device=self.device)
        model_output = self.model(tokenized_input.input_ids, attention_mask=tokenized_input.attention_mask)

        orthobiase_vectors = model_output[1][:len(self.classes)]
        result = model_output[1][len(self.classes):]

        tokenized_input.to("cpu")
        del tokenized_input
        del model_output

        return [x.item() for x in cosine(orthobiase_vectors, result)]


some_list = ["Разработчик FastApi", "Продавец", "Дворник"]
a = DeepPavlovClassificator(some_list)
#b = ZeroShotClassisficator(some_list)
print(a.predict("Программист дворцов"))
#print(b.predict("Программист"))
