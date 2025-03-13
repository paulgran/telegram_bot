import logging
import asyncio
import os
import openai
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

# Загрузка API-ключей
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise ValueError("❌ Ошибка: TELEGRAM_BOT_TOKEN не загружен!")
if not OPENAI_API_KEY:
    raise ValueError("❌ Ошибка: OPENAI_API_KEY не загружен!")

# Инициализация бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

# Логирование
logging.basicConfig(level=logging.INFO)

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Наши услуги"), KeyboardButton(text="💰 Цены")],
        [KeyboardButton(text="📂 Получить документы"), KeyboardButton(text="💳 Оплатить")],
        [KeyboardButton(text="🗓 Забронировать")]
    ],
    resize_keyboard=True
)

# 🟢 Функция для парсинга информации с сайта
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
        logging.error(f"Ошибка парсинга: {e}")
        return "❌ Ошибка при получении информации с сайта."

# 🟢 Функция для общения с GPT
def ask_gpt(user_query):
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

# 🟢 Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добрый день! Мы рады приветствовать вас в нашем Дайв Центре Scuba Birds. Чем могу вам помочь?", 
        reply_markup=main_keyboard
    )

# 🟢 Обработчики кнопок
@dp.message(F.text == "📋 Наши услуги")
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

@dp.message(F.text == "💰 Цены")
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

@dp.message(F.text == "📂 Медицинская форма")
async def send_documents(message: types.Message):
    document_path = "medical_form.pdf"  
    if os.path.exists(document_path):
        await message.answer_document(types.FSInputFile(document_path), caption="📎 Вот ваш документ!")
    else:
        await message.answer("❌ Документ не найден! Пожалуйста, свяжитесь с администрацией.")

@dp.message(F.text == "💳 Оплатить")
async def payment_link(message: types.Message):
    text = (
        "💳 Оплатить можно по ссылке:\n\n"
        '<a href="https://wise.com/pay/business/scubabirdscoltd">Оплата</a>'
    )
    await message.answer(text)

@dp.message(F.text == "🗓 Забронировать")
async def booking(message: types.Message):
    text = (
        "🗓 <b>Бронирование</b>\n\n"
        "🔹 Забронировать онлайн: <a href='https://www.scubabirds.com/booking-now.html'>Scuba Birds Booking</a>\n"
        "🔹 Написать в WhatsApp: <a href='https://wa.me/66990307571'>+66 990 307 571</a>\n\n"
        "Выберите удобный способ бронирования!"
    )
    await message.answer(text)

# 🟢 Обработчик любых других сообщений (GPT отвечает на вопросы)
@dp.message()
async def gpt_response(message: types.Message):
    user_query = message.text
    response = ask_gpt(user_query)
    
    # Если ответ слишком длинный, разбиваем на части
    if len(response) > 4000:
        for i in range(0, len(response), 4000):
            await message.answer(response[i:i+4000])
    else:
        await message.answer(response)

# 🟢 Запуск бота
async def main():
    logging.info("✅ Бот запущен!")
    async with bot:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())