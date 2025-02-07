import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Укажите ваш Telegram Bot Token
TOKEN = "YOUR_BOT_TOKEN"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Логирование
logging.basicConfig(level=logging.INFO)

# Клавиатура для главного меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📅 Забронировать дайвинг"))
main_menu.add(KeyboardButton("ℹ️ Частые вопросы"))
main_menu.add(KeyboardButton("💳 Оплата"))
main_menu.add(KeyboardButton("📍 Локация дайв-центра"))

# Часто задаваемые вопросы
faq_text = """❓ Часто задаваемые вопросы:
1️⃣ Какие программы у вас есть?
   - Пробное погружение (Try Diving) – 1,800 THB
   - Курс Open Water Diver – 8,890 THB
   - Курс Advanced – 8,490 THB

2️⃣ Что включено в стоимость?
   ✅ Прокат снаряжения
   ✅ Инструктор PADI
   ✅ Легкие закуски, чай/кофе, вода
   ✅ Страховка

3️⃣ Какие методы оплаты?
   - Wise: https://wise.com_ссылка
   - PayPal: https://paypal.meссылка
   - Наличными на месте

4️⃣ Где находится ваш дайв-центр?
   📍 [Google Maps](https://maps.app.goo.gl/dw5MsmvDowu3RSqF9)
"""

# Хендлер для команды /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("👋 Привет! Я бот дайв-центра Scuba Birds.\nВыберите действие:", reply_markup=main_menu)

# Хендлер для кнопки "Частые вопросы"
@dp.message_handler(lambda message: message.text == "ℹ️ Частые вопросы")
async def faq(message: types.Message):
    await message.answer(faq_text, parse_mode="Markdown")

# Хендлер для кнопки "Забронировать дайвинг"
@dp.message_handler(lambda message: message.text == "📅 Забронировать дайвинг")
async def booking(message: types.Message):
    await message.answer("📌 Выберите программу:\n"
                         "1️⃣ Try Diving - 1,800 THB\n"
                         "2️⃣ Open Water Diver - 8,890 THB\n"
                         "3️⃣ Advanced Open Water - 8,490 THB\n\n"
                         "💬 Напишите мне название программы и дату!")

# Хендлер для кнопки "Оплата"
@dp.message_handler(lambda message: message.text == "💳 Оплата")
async def payment(message: types.Message):
    await message.answer("💰 Вы можете внести предоплату 400 THB:\n\n"
                         "🔹 Wise: [ссылка](https://wise.com_ссылка)\n"
                         "🔹 PayPal: [ссылка](https://paypal.meссылка)\n"
                         "Оставшуюся сумму можно оплатить на месте.")

# Хендлер для кнопки "Локация дайв-центра"
@dp.message_handler(lambda message: message.text == "📍 Локация дайв-центра")
async def location(message: types.Message):
    await message.answer("📍 Наш дайв-центр находится на Ко Тао:\n"
                         "[Google Maps](https://maps.app.goo.gl/dw5MsmvDowu3RSqF9)")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
