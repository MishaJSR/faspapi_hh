import torch
from torch import nn
from transformers import AutoTokenizer, AutoModel
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased-sentence")
model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased-sentence")

SERVING_VECTORS_NAMES = ["Критическая инфраструктура", "Люди, личности, персоны", "Военная техника, вооружение"]

input_string = ["Курская АЭС на шашлыках", "Русня пишет, отработала ПВО в Курчатово", "БМП крутая тема",
                "Владимир Владимирович Путин"]
INPUT_COUNT = len(input_string)

for item in SERVING_VECTORS_NAMES[::-1]:
    input_string.insert(0, item)

tokenized_input = tokenizer(input_string, padding=True, return_tensors='pt')
model_output = model(tokenized_input.input_ids, attention_mask=tokenized_input.attention_mask)

orthobiase_vectors = model_output[1][:len(SERVING_VECTORS_NAMES)]
results = model_output[1][len(SERVING_VECTORS_NAMES):]

cos = nn.CosineSimilarity(-1)


def countSimmilarity(orthobiase_vectors, result):
    simmilarity = cos(orthobiase_vectors, result)

    return [x.item() for x in simmilarity]


def formStatsDataFrame(data, columns, simmilarities):
    return pd.DataFrame(index=[data], data=simmilarities, columns=[columns])


def processText(orthobiase_vectors, results):
    data = []
    simmilarities = []
    columns = SERVING_VECTORS_NAMES

    for index in range(INPUT_COUNT):
        simmilarities.append(countSimmilarity(orthobiase_vectors, result=results[index]))
        data.append(input_string[INPUT_COUNT + index - 1])

    return data, simmilarities, columns


data, simmilarities, columns = processText(orthobiase_vectors=orthobiase_vectors, results=results)
pass

formStatsDataFrame(data=data, columns=columns, simmilarities=simmilarities)
