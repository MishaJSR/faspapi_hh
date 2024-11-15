import asyncio
import json
from copyreg import constructor
from threading import Lock

import logging
import aio_pika

from base_settings import base_settings
from rabbit_utils.RabbitMQFactory import FastRMQDataObject


class RabbitSingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Rabbit(metaclass=RabbitSingletonMeta):
    _queue_list = ["from_fastapi"]
    _connection = None
    _queue = {
        "from_fastapi": FastRMQDataObject
    }

    async def connect(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(
                f"amqp://guest:guest@{base_settings.get_ampq_host()}/"
            )
        async with self._connection:
            logging.info(f"Server RabbitMQ listen on {base_settings.get_ampq_host()}")
            channel = await self._connection.channel()
            await channel.set_qos(prefetch_count=10)
            tasks = []
            for queue_name in self._queue_list:
                queue = await channel.declare_queue(queue_name, durable=True)
                task = asyncio.create_task(self.listen_to_queue(queue, queue_name))
                tasks.append(task)
            await asyncio.gather(*tasks)

    async def close(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None
            logging.info("Подключение закрыто.")

    async def listen_to_queue(self, queue, queue_name: str) -> None:
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self.process_message(queue_name, message)

    async def process_message(self, queue_name: str, message) -> None:
        message_body = message.body.decode('utf-8')
        data = json.loads(message_body)
        construct_factory = self._queue.get(queue_name)
        if not construct_factory:
            logging.info(f"Received from unsigned query {queue_name}: {data}")
        else:
            await construct_factory.get_custom_object(data=data).operation()
