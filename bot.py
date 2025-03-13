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

# 🔹 Функция общения с GPT (исправлена)
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
        return "❌ Ошибка: OpenAI временно недоступен. Попробуйте позже."

    except Exception as e:
        logging.error(f"❌ Неизвестная ошибка: {e}")
        return "❌ Ошибка сервера. Попробуйте позже."

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
        "3️⃣ Нырялка для сертифицированных дайверов\n"
        "4️⃣ Продолжить обучение дайвингу\n"
        "5️⃣ Обучение профессионалов (Dive Master/Instructor)\n\n"
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

# 🔹 Отправка мед. справки
@dp.message(lambda message: message.text and "мед справка" in message.text.lower())
async def send_medical_form(message: types.Message):
    document_path = "medical_form.pdf"  # Укажите правильное имя файла

    if os.path.exists(document_path):
        await message.answer_document(types.FSInputFile(document_path), caption="📎 Вот ваша медицинская справка!")
    else:
        await message.answer("❌ Медицинская справка не найдена! Свяжитесь с администрацией.")

# 🔹 Кнопка бронирования
@dp.message(lambda message: message.text and "забронировать" in message.text.lower())
async def booking(message: types.Message):
    text = (
        "🗓 <b>Бронирование</b>\n\n"
        "🔹 Забронировать онлайн: <a href='https://www.scubabirds.com/booking-now.html'>Scuba Birds Booking</a>\n"
        "🔹 Написать в WhatsApp: <a href='https://wa.me/66990307571'>+66 990 307 571</a>\n\n"
        "Выберите удобный способ бронирования!"
    )
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

# 🔹 GPT отвечает на вопросы
@dp.message()
async def gpt_response(message: types.Message):
    user_query = message.text
    response = ask_gpt(user_query)
    
    for i in range(0, len(response), 4000):
        await message.answer(response[i:i+4000])

# 🔹 Запуск бота и сервера
async def start_bot():
    logging.info("✅ Бот запущен!")
    await dp.start_polling(bot)

def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

async def main():
    loop = asyncio.get_running_loop()
    bot_task = loop.create_task(start_bot())
    server_task = loop.run_in_executor(None, start_fastapi)
    await asyncio.gather(bot_task, server_task)

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")