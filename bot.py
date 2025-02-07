import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем токен из .env файла
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Настраиваем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Кнопки главного меню
menu_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
menu_buttons.add(KeyboardButton("📋 Курсы"), KeyboardButton("💬 Частые вопросы"))
menu_buttons.add(KeyboardButton("📅 Бронирование"), KeyboardButton("💰 Оплата"))

# Ответы на вопросы
FAQ = {
    "Как забронировать курс?": "Чтобы забронировать курс, сделайте предоплату 400฿ и отправьте свои данные (имя, дату рождения, email).",
    "Какие курсы вы предлагаете?": "Мы предлагаем PADI Open Water Diver, Advanced Open Water и другие. Напишите /courses для подробной информации.",
    "Как оплатить?": "Вы можете сделать предоплату через Wise или PayPal. Ссылки на оплату отправим после бронирования.",
    "Где находится дайв-центр?": "Наш дайв-центр находится на Ко Тао. Адрес: https://maps.app.goo.gl/dw5MsmvDowu3RSqF9"
}

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! 🤿 Добро пожаловать в PADI 5 Star Scuba Birds Dive Center! Чем могу помочь?", reply_markup=menu_buttons
    )

# Команда /faq
@dp.message_handler(lambda message: message.text == "💬 Частые вопросы")
async def send_faq(message: types.Message):
    faq_text = "Часто задаваемые вопросы:\n\n"
    for q in FAQ.keys():
        faq_text += f"🔹 {q}\n"
    faq_text += "\nВыберите вопрос или напишите его в чат."
    await message.answer(faq_text)

# Ответы на частые вопросы
@dp.message_handler(lambda message: message.text in FAQ.keys())
async def answer_faq(message: types.Message):
    await message.answer(FAQ[message.text])

# Команда /courses
@dp.message_handler(lambda message: message.text == "📋 Курсы")
async def send_courses(message: types.Message):
    text = (
        "📘 Наши курсы:\n\n"
        "🔹 Open Water Diver - ฿8,890 (2.5 дня)\n"
        "🔹 Advanced Open Water - ฿8,490 (2 дня)\n"
        "🔹 Discover Scuba Diving - ฿1,800 (1 погружение) или ฿2,800 (2 погружения)\n\n"
        "Выберите курс и напишите мне для бронирования! 🤿"
    )
    await message.answer(text)

# Команда /booking
@dp.message_handler(lambda message: message.text == "📅 Бронирование")
async def book_course(message: types.Message):
    await message.answer(
        "Чтобы забронировать курс, пришлите:\n\n"
        "1️⃣ Ваше имя и фамилию\n"
        "2️⃣ Дату рождения (дд-мм-гггг)\n"
        "3️⃣ Email\n"
        "4️⃣ Название курса\n\n"
        "После этого мы отправим вам ссылку на предоплату. 💰"
    )

# Команда /payment
@dp.message_handler(lambda message: message.text == "💰 Оплата")
async def send_payment_info(message: types.Message):
    text = (
        "💰 Оплата:\n\n"
        "🔹 Wise: https://wise.com_ссылка\n"
        "🔹 PayPal: https://paypal.me_ссылка\n\n"
        "После предоплаты отправьте чек, чтобы подтвердить платеж."
    )
    await message.answer(text)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
