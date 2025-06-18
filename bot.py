print("✅ Новый bot.py загружен")
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
import asyncio
import json
from config import TELEGRAM_TOKEN, OPENAI_API_KEY, GPT_MODEL
import openai
from usage import check_and_update_usage, reset_usage
from logger import log_message
from langs import get_text, set_lang, get_lang
from stats import log_user

openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
ADMIN_ID = 381103315
PAY_LINK = "https://t.me/newgptbot_bot"

def get_main_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("ask", lang))],
            [KeyboardButton(text=get_text("change_lang", lang)), KeyboardButton(text=get_text("reset_limit", lang))]
        ],
        resize_keyboard=True
    )

@dp.message(CommandStart())
async def start_handler(message: Message):
    log_user(str(message.from_user.id), message.from_user.username)
    await message.answer("🌐 Choose your language / Выберите язык:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True
    ))

@dp.message(lambda m: m.text in ["🇷🇺 Русский", "🇬🇧 English"])
async def set_language(message: Message):
    lang = "ru" if "Русский" in message.text else "en"
    set_lang(str(message.from_user.id), lang)
    await message.answer(get_text("welcome", lang), reply_markup=get_main_menu(lang))

@dp.message(lambda m: m.text in ["Задать вопрос", "Ask a question"])
async def ask_mode(message: Message):
    lang = get_lang(str(message.from_user.id))
    await message.answer(get_text("ask_prompt", lang), reply_markup=get_main_menu(lang))

@dp.message(lambda m: m.text == get_text("reset_limit", get_lang(str(m.from_user.id))))
async def reset_limit_prompt(message: Message):
    lang = get_lang(str(message.from_user.id))
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("pay_button", lang), url=PAY_LINK)]
    ])
    await message.answer(get_text("manual_payment", lang), reply_markup=kb)

@dp.message(Command("approve"))
async def manual_approve(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Нет доступа.")
        return
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("❗ Используй формат: /approve <user_id>")
        return
    uid = parts[1]
    reset_usage(uid)
    await message.answer(f"✅ Лимит для пользователя {uid} сброшен.")

@dp.message()
async def gpt_handler(message: Message):
    user_id = str(message.from_user.id)
    lang = get_lang(user_id)
    if not check_and_update_usage(user_id):
        await reset_limit_prompt(message)
        return
    await message.answer(get_text("thinking", lang))
    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response.choices[0].message.content
        await message.answer(reply)
        log_message(user_id, message.text, reply)
    except Exception:
        await message.answer(get_text("error", lang))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
except Exception as e:
    import logging
    logging.error(f'[GPT ERROR] {e}')
    reply = '❌ Ошибка при обращении к GPT. Попробуйте позже.'