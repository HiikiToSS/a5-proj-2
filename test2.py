import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton
from dotenv import load_dotenv


import os
import time

import requests
from dotenv import load_dotenv


ikb = InlineKeyboardButton("Перейти", web_app=WebAppInfo('https://<your_domain>'))
kb = KeyboardButton("Перейти", web_app=WebAppInfo('https://<your_domain>'))


async def test(message: Message) -> None:
    await message.answer('Вот тест, лови:')


async def check(message: Message) -> None:
    await message.answer('че-как?')

async def start(message: Message) -> None:
    await message.answer('Привет, какая тема для теста?')

async def echo(message: Message) -> None:
    await message.answer(message.text)

async def main() -> None:
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    dp = Dispatcher()

    dp.message.register(check, Command('чк'))
    dp.message.register(test, Command('тема'))
    dp.message.register(start, Command('start'))
    dp.message.register(echo, F.text)
    bot = Bot(token=bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())