import asyncio
from concurrent.futures import ThreadPoolExecutor


# Асинхронная функция
async def async_function(value):
    await asyncio.sleep(1)  # Имитация длительной операции
    return f"Результат для {value}"


# Функция-обертка для запуска асинхронной функции
def run_async_function(value):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_function(value))
    loop.close()
    return result


# Основной код
values = [1, 2, 3, 4, 5]  # Пример списка значений

results = []
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(run_async_function, value) for value in values]

    for future in futures:
        results.append(future.result())  # Дождаться завершения каждого потока

print(results)