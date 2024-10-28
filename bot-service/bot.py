import logging
import asyncio
import threading

import grpc
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
import betterlogging as bl

from base_settings import base_settings
from handlers.user.user_main_router import user_main_router
from grpc_service import message_pb2_grpc, message_pb2


class MessageService(message_pb2_grpc.MessageServiceServicer):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def SendMessage(self, request, context):
        await self.bot.send_message(chat_id=548349299, text=request.text)
        logging.info(f"Get message {request.text}")
        return message_pb2.Message(text='Message sent')




def get_storage():
    if base_settings.is_use_redis():
        return RedisStorage.from_url(
            base_settings.get_redis_storage(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )


async def on_startup():
    logging.info("Starting bot")


async def on_shutdown(bot):
    logging.info("Shutdown bot")


async def serve(bot):
    server = grpc.aio.server()
    message_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(bot), server)
    server.add_insecure_port('[::]:50051')
    logging.info("server grpc start")
    await server.start()
    await server.wait_for_termination()


async def main():
    bot, dp = await set_bot()
    await asyncio.gather(serve(bot), start_bot(bot, dp))


async def grpc_listener():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = message_pb2_grpc.MessageServiceStub(channel)
        await stub.SendMessage(message_pb2.Message(text="Hello from gRPC!"))


async def set_bot():
    setup_logging()
    storage = get_storage()
    bot = Bot(token=base_settings.get_token())
    dp = Dispatcher(storage=storage)
    dp.include_routers(user_main_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return bot, dp


async def start_bot(bot, dp):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=[BotCommand(command='start', description='Запустить бота')],
                           scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)




if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())









