from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, PreCheckoutQuery
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
import asyncio
import json
from config import TELEGRAM_TOKEN, GPT_API_KEY, GPT_MODEL, PAYMENT_TOKEN
import openai
from usage import check_and_update_usage, reset_usage
from logger import log_message
from langs import get_text, set_lang, get_lang
from stats import log_user

openai.api_key = GPT_API_KEY

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

PRICE = types.LabeledPrice(label="GPT-доступ без ограничений", amount=9900)  # 99.00 THB

def get_main_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("ask", lang))],
            [KeyboardButton(text=get_text("change_lang", lang)), KeyboardButton(text=get_text("reset_limit", lang))]
        ],
        resize_keyboard=True
    )

lang_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start_handler(message: Message):
    log_user(str(message.from_user.id), message.from_user.username)
    await message.answer("🌐 Choose your language / Выберите язык:", reply_markup=lang_keyboard)

@dp.message(Command("lang"))
async def lang_handler(message: Message):
    await message.answer("🌐 Choose your language / Выберите язык:", reply_markup=lang_keyboard)

@dp.message(lambda m: m.text in ["🇷🇺 Русский", "🇬🇧 English"])
async def set_language(message: Message):
    user_id = str(message.from_user.id)
    lang_code = "ru" if "Русский" in message.text else "en"
    set_lang(user_id, lang_code)
    await message.answer(get_text("welcome", lang_code), reply_markup=get_main_menu(lang_code))

@dp.message(lambda m: m.text in ["Задать вопрос", "Ask a question"])
async def ask_mode(message: Message):
    lang = get_lang(str(message.from_user.id))
    await message.answer(get_text("ask_prompt", lang), reply_markup=get_main_menu(lang))

@dp.message(lambda m: m.text in ["Сменить язык", "Change language"])
async def change_language(message: Message):
    await lang_handler(message)

@dp.message(lambda m: m.text in ["Сбросить лимит", "Reset limit"])
async def pay_limit(message: Message):
    lang = get_lang(str(message.from_user.id))
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="GPT Assistant",
        description=get_text("payment_description", lang),
        provider_token=PAYMENT_TOKEN,
        currency="THB",
        prices=[PRICE],
        start_parameter="gpt-access",
        payload="limit_reset"
    )

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message(lambda m: m.successful_payment)
async def process_successful_payment(message: Message):
    reset_usage(str(message.from_user.id))
    lang = get_lang(str(message.from_user.id))
    await message.answer(get_text("payment_success", lang), reply_markup=get_main_menu(lang))

@dp.message()
async def gpt_handler(message: Message):
    user_id = str(message.from_user.id)
    lang = get_lang(user_id)

    if not check_and_update_usage(user_id):
        await pay_limit(message)
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
    except Exception as e:
        await message.answer(get_text("error", lang))from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from stats import get_all_users

ADMIN_ID = 381103315  # Замените на ваш Telegram ID

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Список пользователей")]
    ],
    resize_keyboard=True
)

@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Нет доступа.")
        return
    await message.answer("👤 Админ-панель", reply_markup=admin_menu)

@dp.message(lambda m: m.from_user.id == ADMIN_ID and m.text == "📋 Список пользователей")
async def list_users(message: Message):
    users = get_all_users()
    if not users:
        await message.answer("Нет зарегистрированных пользователей.")
        return
    text = "📊 Пользователи:

"
    for uid, data in users.items():
        text += f"• ID: {uid}
  Username: @{data.get('username', '—')}
  Дата входа: {data['joined']}

"
    await message.answer(text)