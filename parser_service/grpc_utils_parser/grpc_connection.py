import grpc

from base_settings import base_settings
from grpc_utils_parser import message_pb2_grpc, message_pb2


async def send_grpc_to_tg(**kwargs):
    name = kwargs.get("name")
    url = kwargs.get("url")
    salary = kwargs.get("salary")
    employer = kwargs.get("employer")
    tg_user_id = kwargs.get("tg_user_id")
    text = f"{name}\n{url}\n{salary}\n{employer}"
    async with grpc.aio.insecure_channel(f'{base_settings.get_grpc_host()}:50051') as channel:
        stub = message_pb2_grpc.MessageServiceStub(channel)
        response = await stub.SendMessage(message_pb2.Message(text=text, tg_user_id=tg_user_id))
    return response.text