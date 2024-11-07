import asyncio
import json
import logging

import aio_pika


async def process_message(queue_name: str, message) -> None:
    # Преобразуем тело сообщения в строку
    message_body = message.body.decode('utf-8')
    data = json.loads(message_body)  # Преобразуем JSON строку в словарь

    # Выполняем функционал в зависимости от имени очереди
    print(f"Received message from {queue_name}: {data}")

    # Пример: обработка по имени очереди
    if queue_name == "test_queue":
        # Обрабатываем сообщения из "queue_1"
        print("Handling message from queue_1...")
    elif queue_name == "queue_2":
        # Обрабатываем сообщения из "queue_2"
        print("Handling message from queue_2...")
    else:
        print("Handling message from unknown queue...")


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@172.18.0.3/",
    )

    async with connection:
        # Создаем канал
        channel = await connection.channel()

        # Настройка QoS
        await channel.set_qos(prefetch_count=10)

        # Список очередей
        queue_names = ["queue_1", "queue_2", "test_queue"]  # Пример списка очередей

        # Слушаем все очереди одновременно
        tasks = []
        for queue_name in queue_names:
            # Объявляем очереди
            queue = await channel.declare_queue(queue_name, auto_delete=True)

            # Создаем задачу для прослушивания очереди
            task = asyncio.create_task(listen_to_queue(queue, queue_name))
            tasks.append(task)

        # Ожидаем завершения всех задач
        await asyncio.gather(*tasks)


async def listen_to_queue(queue, queue_name: str) -> None:
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                await process_message(queue_name, message)


if __name__ == "__main__":
    asyncio.run(main())
