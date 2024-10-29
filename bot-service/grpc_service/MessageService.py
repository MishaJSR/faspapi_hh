import logging

from aiogram import Bot

from grpc_service import message_pb2_grpc, message_pb2


class MessageService(message_pb2_grpc.MessageServiceServicer):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def SendMessage(self, request, context):
        await self.bot.send_message(chat_id=request.tg_user_id, text=request.text)
        logging.info(f"Get message {request.text}")
        return message_pb2.Message(text='Message sent')