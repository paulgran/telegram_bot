import logging
import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import asyncio

from config import OPENAI_API_KEY, TELEGRAM_TOKEN, GPT_MODEL

logging.basicConfig(level=logging.INFO)

openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Задать вопрос")],
            [KeyboardButton(text="Сменить язык"), KeyboardButton(text="Сбросить лимит")]
        ],
        resize_keyboard=True
    )

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("🌐 Choose your language / Выберите язык:", reply_markup=get_main_keyboard())

@dp.message(lambda m: m.text == "Задать вопрос")
async def ask_handler(message: Message):
    await message.answer("Пожалуйста, введите ваш вопрос:")

@dp.message()
async def gpt_handler(message: Message):
    user_input = message.text
    await message.answer("✍️ Думаю...")

    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logging.error(f"[GPT ERROR] {e}")
        reply = "❌ Ошибка при запросе к GPT. Проверь API-ключ или лимит использования."

    await message.answer(reply)

async def main():
    print("✅ Новый bot.py загружен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
