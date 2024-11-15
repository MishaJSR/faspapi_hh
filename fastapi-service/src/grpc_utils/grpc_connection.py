from random import randint

import grpc
import logging
import asyncio
import random

from base_settings import base_settings
from grpc_utils import message_pb2_grpc, message_pb2


async def send_grpc_to_tg(**kwargs):
    name = kwargs.get("name")
    url = kwargs.get("url")
    salary = kwargs.get("salary")
    employer = kwargs.get("employer")
    user_tg_id = kwargs.get("user_tg_id")
    text = f"{name}\n{url}\n{salary}\n{employer}"
    async with grpc.aio.insecure_channel(f'{base_settings.get_grpc_host()}:50051') as channel:
        stub = message_pb2_grpc.MessageServiceStub(channel)
        await asyncio.sleep(random.randint(1, 5))
        logging.info(f"Sending vac for {user_tg_id}...")
        response = await stub.SendMessage(message_pb2.Message(text=text, tg_user_id=user_tg_id))
        logging.info(f"Status {name} for {user_tg_id} - {response.text}")
    return response.text
