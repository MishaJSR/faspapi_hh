import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
import betterlogging as bl

from base_settings import base_settings
from grpc_utils.grpc_server import serve_grpc
from handlers.user.user_main_router import user_main_router
from rabbit_utils.Rabbit import Rabbit


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


def on_startup():
    logging.info("Starting bot")


def on_shutdown(bot):
    logging.info("Shutdown bot")


async def main():
    bot, dp = await create_bot()
    rabbit = Rabbit()
    await asyncio.gather(serve_grpc(bot), rabbit.connect(), start_bot(bot, dp))


async def create_bot():
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
