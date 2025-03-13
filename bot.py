import logging
import asyncio
import os
import openai
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from fastapi import FastAPI
import uvicorn

# 🔹 Загрузка API-ключей
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise ValueError("❌ Ошибка: TELEGRAM_BOT_TOKEN не загружен!")
if not OPENAI_API_KEY:
    raise ValueError("❌ Ошибка: OPENAI_API_KEY не загружен!")

# 🔹 Инициализация бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

# 🔹 Логирование
logging.basicConfig(level=logging.INFO)

# 🔹 Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Наши услуги"), KeyboardButton(text="💰 Цены")],
        [KeyboardButton(text="📂 Мед справка"), KeyboardButton(text="💳 Оплатить")],
        [KeyboardButton(text="🗓 Забронировать")]
    ],
    resize_keyboard=True
)

# 🔹 Создаём FastAPI-сервер
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Бот работает!"}

# 🔹 Функция парсинга информации с сайта
def get_info_from_scubabirds():
    url = "https://www.scubabirds.ru/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')  
            text_content = " ".join([p.get_text() for p in paragraphs])
            return text_content[:1500]  # Ограничим до 1500 символов
        return "Ошибка при получении данных с сайта."
    except Exception as e:
        logging.error(f"❌ Ошибка парсинга: {e}")
        return "❌ Ошибка при получении информации с сайта."

# 🔹 Функция общения с GPT (с обработкой ошибок)
def ask_gpt(user_query):
    try:
        site_info = get_info_from_scubabirds()
        
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты помощник, который отвечает на вопросы о дайвинге."},
                {"role": "user", "content": f"Вот информация с сайта Scuba Birds: {site_info}. Теперь ответь на вопрос: {user_query}"}
            ]
        )
        return response["choices"][0]["message"]["content"]

    except openai.error.OpenAIError as e:
        logging.error(f"❌ Ошибка OpenAI: {e}")
        return "❌ Ошибка при получении ответа от GPT."

# 🔹 Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добрый день! Мы рады приветствовать вас в нашем Дайв Центре Scuba Birds. Чем могу вам помочь?", 
        reply_markup=main_keyboard
    )

# 🔹 Обработчики кнопок
@dp.message(lambda message: message.text and "услуги" in message.text.lower())
async def services(message: types.Message):
    text = (
        "📌 Мы предлагаем следующие услуги:\n"
        "1️⃣ Пробное погружение\n"
        "2️⃣ Получение первичного сертификата Дайвера\n"
        "3️⃣ Fun Diving\n"
        "4️⃣ Продолжить обучение дайвингу\n"
        "5️⃣ Обучение профессионалов\n\n"
        "Ознакомьтесь с нашими ценами в разделе <b>Цены</b>!"
    )
    await message.answer(text)

@dp.message(lambda message: message.text and "цены" in message.text.lower())
async def prices(message: types.Message):
    text = (
        "💰 Наши цены:\n\n"
        "🔹 <b>Пробное погружение</b> — 2,800 TBH \n"
        "🔹 <b>Курс Open Water Diver</b> (до 18 метров) — 8,990 TBH \n"
        "🔹 <b>Курс Advance Open Water Diver</b> — 8,490 THB \n"
        "🔹 <b>Курс Rescue Diver</b> — 8,500 THB \n"
        "🔹 <b>Курс Dive Master</b> — от 35,000 THB \n\n"
        "Свяжитесь с нами для заказа!"
    )
    await message.answer(text)

# 🔹 GPT отвечает на вопросы
@dp.message()
async def gpt_response(message: types.Message):
    user_query = message.text
    response = ask_gpt(user_query)
    
    # Если ответ слишком длинный, разбиваем на части
    for i in range(0, len(response), 4000):
        await message.answer(response[i:i+4000])

# 🔹 Запуск бота
async def start_bot():
    logging.info("✅ Бот запущен!")
    await dp.start_polling(bot)

# 🔹 Запуск FastAPI
def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

# 🔹 Запуск бота и сервера
async def main():
    loop = asyncio.get_running_loop()
    bot_task = loop.create_task(start_bot())  # Запуск бота
    server_task = loop.run_in_executor(None, start_fastapi)  # Запуск сервера в отдельном потоке
    await asyncio.gather(bot_task, server_task)

# 🔹 Запуск (с обработкой ошибок)
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())  # 🔥 Исправлено!
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")