from sentence_transformers import SentenceTransformer, util

# Загружаем модель
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Модель загружена")
# Ваши контексты
context_1 = "Кошки очень независимые животные."
context_2 = "Многие домашние питомцы предпочитают проводить время одни."

# Кодируем контексты
embedding_1 = model.encode(context_1, convert_to_tensor=True)
embedding_2 = model.encode(context_2, convert_to_tensor=True)

# Вычисляем косинусное сходство
cosine_score = util.pytorch_cos_sim(embedding_1, embedding_2)

print(f"Сходство между контекстами: {cosine_score.item():.4f}")