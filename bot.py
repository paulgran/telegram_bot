import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties  # ✅ Добавлен импорт DefaultBotProperties

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Ошибка: TELEGRAM_BOT_TOKEN не загружен!")

# ✅ Исправлено: передаём parse_mode через DefaultBotProperties
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём клавиатуру с кнопками
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Наши услуги"), KeyboardButton(text="💰 Цены")],
        [KeyboardButton(text="📂 Получить документы"), KeyboardButton(text="💳 Оплатить")],
        [KeyboardButton(text="🗓 Забронировать")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добрый день! Мы рады приветствовать вас в нашем Дайв Центре Scuba Birds. Чем могу вам помочь?", 
        reply_markup=main_keyboard
    )

# Информация об услугах
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

# Отправка цен
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

# Отправка документов
@dp.message(F.text == "📂 Получить документы")
async def send_documents(message: types.Message):
    document_path = "medical_form.pdf"  # Путь к файлу
    if os.path.exists(document_path):
        await message.answer_document(types.FSInputFile(document_path), caption="📎 Вот ваш документ!")
    else:
        await message.answer("❌ Документ не найден! Пожалуйста, свяжитесь с администрацией.")

# Отправка ссылки на оплату
@dp.message(F.text == "💳 Оплатить")
async def payment_link(message: types.Message):
    text = (
        "💳 Оплатить можно по ссылке:\n\n"
        '<a href="https://wise.com/pay/business/scubabirdscoltd">Оплата</a>'
    )
    await message.answer(text)

# Обработчик кнопки "Забронировать"
@dp.message(F.text == "🗓 Забронировать")
async def booking(message: types.Message):
    text = (
        "🗓 <b>Бронирование</b>\n\n"
        "🔹 Забронировать онлайн: <a href='https://www.scubabirds.com/booking-now.html'>Scuba Birds Booking</a>\n"
        "🔹 Написать в WhatsApp: <a href='https://wa.me/66990307571'>+66 990 307 571</a>\n\n"
        "Выберите удобный способ бронирования!"
    )
    await message.answer(text)

# Функция для запуска бота
async def main():
    logging.info("✅ Бот запущен!")
    async with bot:
        await dp.start_polling(bot)

# Запуск бота через asyncio
if __name__ == "__main__":
    asyncio.run(main())