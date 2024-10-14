import asyncio

from base_settings import base_settings

from telegram import Bot

bot = Bot(token=base_settings.get_api_token())
