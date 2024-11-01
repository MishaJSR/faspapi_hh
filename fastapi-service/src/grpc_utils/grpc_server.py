import logging

import grpc

from grpc_utils import message_pb2_grpc, message_pb2
from grpc_utils.MessageService import MessageService


async def serve(bot):
    server = grpc.aio.server()
    message_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(bot), server)
    server.add_insecure_port('[::]:50051')
    logging.info("server grpc start")
    await server.start()
    await server.wait_for_termination()


async def grpc_listener():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = message_pb2_grpc.MessageServiceStub(channel)
        await stub.SendMessage(message_pb2.Message(text="Hello from gRPC!"))