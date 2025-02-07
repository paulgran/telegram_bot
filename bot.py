import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Ошибка: TELEGRAM_BOT_TOKEN не загружен!")


# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём клавиатуру с кнопками
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Наши услуги"), KeyboardButton(text="💰 Цены")],
        [KeyboardButton(text="📂 Получить документы"), KeyboardButton(text="💳 Оплатить")]
    ],
    resize_keyboard=True)

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Добрый день! Мы рады приветствовать вас в нашем Дайв Центре Scuba Birds. Чем могу вам помочь?", reply_markup=main_keyboard)

# Информация об услугах
@dp.message(lambda message: message.text == "📋 Наши услуги")
async def services(message: types.Message):
    text = "📌 Мы предлагаем следующие услуги:\n" \
           "1️⃣ Пробное погружение\n" \
           "2️⃣ Получение первичного сертификата Дайвера\n" \
           "3️⃣ Fun Diving\n\n" \
           "Ознакомьтесь с нашими ценами в разделе Цены!"
    await message.answer(text)

# Отправка цен
@dp.message(lambda message: message.text == "💰 Цены")
async def prices(message: types.Message):
    text = "💰 Наши цены:\n\n" \
           "🔹 Пробное погружение — 2,800 TBH \n" \
           "🔹 Курс Open Water Diver (до 18 метров) — 8,990 TBH \n" \
           "🔹 Курс Advance Open Water Diver — 8,490 THB \n" \
           "🔹 Курс Rescue Diver — 8,500 THB \n\n" \
           "Свяжитесь с нами для заказа!"
    await message.answer(text)

# Отправка документов
@dp.message(lambda message: message.text == "📂 Получить документы")
async def send_documents(message: types.Message):
    document_path = "medical_form.pdf"  # Путь к файлу
    with open(document_path, "rb") as doc:
        await message.answer_document(doc, caption="📎 Вот ваш документ!")

# Отправка ссылки на оплату
@dp.message(lambda message: message.text == "💳 Оплатить")
async def payment_link(message: types.Message):
    text = "💳 Оплатить можно по ссылке:\n\n" \
           "[Оплата](https://wise.com/pay/business/scubabirdscoltd)"
    await message.answer(text, parse_mode="Markdown")

# Функция для запуска бота
async def main():
    await dp.start_polling(bot)

# Запуск бота через asyncio
if __name__ == "__main__":
    asyncio.run(main())
