import grpc

from grpc_utils import message_pb2_grpc, message_pb2


async def send_grpc_to_tg(name: str, url: str, salary: str, employer: str, tg_user_id: int):
    text = f"{name}\n{url}\n{salary}\n{employer}"
    async with grpc.aio.insecure_channel('tg-bot:50051') as channel:
        stub = message_pb2_grpc.MessageServiceStub(channel)
        response = await stub.SendMessage(message_pb2.Message(text=text, tg_user_id=tg_user_id))
    return response.text