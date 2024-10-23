import requests
from aiogram.filters import CommandStart, Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

user_main_router = Router()


@user_main_router.message(CommandStart())
async def user_start(message: types.Message, state: FSMContext):
    await message.answer("Привет")

