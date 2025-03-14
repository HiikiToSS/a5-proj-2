import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from dotenv import load_dotenv


import os
import time

import requests
from dotenv import load_dotenv

def YanGpt(usrPrompt):
    load_dotenv()
    folder_id = os.getenv("YANDEX_FOLDER_ID")
    api_key = os.getenv("YANDEX_API_KEY")
    gpt_model = 'yandexgpt-lite'

    system_prompt = 'Убери и не используй звёздочки!!!!!!. Создай вопросы с выбором ответа на тему от пользователя и ниже правильные ответы на вопросы'
    user_prompt = usrPrompt

    body = {
        'modelUri': f'gpt://{folder_id}/{gpt_model}',
        'completionOptions': {'stream': False, 'temperature': 0.3, 'maxTokens': 2000},
        'messages': [
            {'role': 'system', 'text': system_prompt},
            {'role': 'user', 'text': user_prompt},
        ],
    }
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Api-Key {api_key}'
    }

    response = requests.post(url, headers=headers, json=body)
    operation_id = response.json().get('id')

    url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {api_key}"}

    while True:
        response = requests.get(url, headers=headers)
        done = response.json()["done"]
        if done:
            break
        time.sleep(2)

    data = response.json()
    answer = data['response']['alternatives'][0]['message']['text']

    return answer


def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Мой хабр", url='https://habr.com/ru/users/yakvenalex/')],
        [InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=yakvenalexx')],
        [InlineKeyboardButton(text="Веб приложение", web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)



def answer_variants():
    questions = YanGpt('sssssss').split('Вопрос')
    inline_kb_list = [
        [InlineKeyboardButton(text=questions[0], url='https://habr.com/ru/users/yakvenalex/')],
        [InlineKeyboardButton(text=questions[1], url='tg://resolve?domain=yakvenalexx')],
        [InlineKeyboardButton(text=questions[2], web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def echo(message: Message) -> None:
    textItself = YanGpt(message.text).replace('*', '')
    await message.answer(textItself)
    # questions = YanGpt(message.text).split('Вопрос')
    # print(type(YanGpt(message.text)))
    # print(questions)
    # await message.answer_photo(FSInputFile()) #фото, которое сгенерено



async def get_inline_btn_link(message: Message) -> None:
    await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=ease_link_kb())

async def test(message: Message) -> None:
    global curr_msg
    curr_msg = message.text
    await message.answer('Вот тест, лови:', reply_markup=answer_variants())


async def check(message: Message) -> None:
    await message.answer('че-как?')

async def start(message: Message) -> None:
    await message.answer('Привет, какая тема для теста?')


async def main() -> None:
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    dp = Dispatcher()

    # dp.message.register(check, Command('чк'))
    # dp.message.register(get_inline_btn_link, Command('инл'))
    # dp.message.register(test, Command('тема '))
    dp.message.register(start, Command('start'))
    dp.message.register(echo, F.text)
    bot = Bot(token=bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
