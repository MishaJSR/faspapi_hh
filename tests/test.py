import asyncio
import concurrent.futures
import time
import random


async def async_function_1(value):
    s = random.randint(1, 5)
    await asyncio.sleep(random.randint(1, 5))
    print(f"I sleep {s} from async_function_1 with value {value}")
    return "s"


async def async_function_2(value):
    s = random.randint(1, 5)
    await asyncio.sleep(random.randint(1, 5))
    print(f"I sleep {s} from async_function_2 with value {value}")
    return "s"


def run_async_functions(value):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result1 = loop.run_until_complete(async_function_1(value))
    result2 = loop.run_until_complete(async_function_2(value))
    return result1, result2


def main(values):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = list(executor.map(lambda args: run_async_functions(args), values))
        print(futures)

    # for future in concurrent.futures.as_completed(futures):
    #     if time.time() - start_time > 20:
    #         print("Ошибка: превышено время ожидания в 5 секунд")
    #         break
    #
    #     try:
    #         result = future.result()
    #     except Exception as e:
    #         print(f"Ошибка при выполнении функции для значения {futures[future]}: {e}")


if __name__ == "__main__":
    values = [1, 2, 3, 4, 5]
    main(values)
