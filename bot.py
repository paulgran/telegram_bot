import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Загружаем токен из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("❌ Ошибка: TELEGRAM_BOT_TOKEN не загружен! Проверьте переменные окружения.")
    exit(1)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём клавиатуру с кнопками
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Наши услуги"), KeyboardButton(text="💰 Цены")],
        [KeyboardButton(text="📂 Получить документы"), KeyboardButton(text="💳 Оплатить")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добрый день! Мы рады приветствовать вас в нашем Дайв Центре *Scuba Birds*.\nЧем могу вам помочь?", 
        parse_mode="Markdown",
        reply_markup=main_keyboard
    )

# Информация об услугах
@router.message(lambda message: message.text == "📋 Наши услуги")
async def services(message: types.Message):
    text = (
        "📌 *Мы предлагаем следующие услуги:*\n\n"
        "1️⃣ [Пробное погружение Discover Scuba Diving](https://www.scubabirds.com/padi-courses/beginners/discover-scuba-diving.html)\n"
        "2️⃣ [Получение первичного сертификата (Scuba Diver / Open Water Diver)](https://www.scubabirds.com/padi-courses/beginners/padi-open-water-diver.html)\n"
        "3️⃣ [Продолжение обучения (Advance Open Water Diver / Rescue Diver)](https://www.scubabirds.com/padi-courses/for-certified-divers/padi-advanced-open-water-diver.html)\n"
        "4️⃣ [Fun Diving](https://www.scubabirds.com/ko-tao/fun-diving-packages.html)\n\n"
        "📌 Более детально с нашими программами погружений вы можете ознакомиться на нашем сайте [здесь](https://www.scubabirds.com/)."
    )
    await message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)

# Отправка цен
@router.message(lambda message: message.text == "💰 Цены")
async def prices(message: types.Message):
    text = (
        "💰 *Наши цены:*\n\n"
        "🔹 [PADI Discover Scuba Diving - 2 800 THB](https://www.scubabirds.com/padi-courses/beginners/discover-scuba-diving.html)\n"
        "🔹 [PADI Scuba Diver - 7 500 THB](https://www.scubabirds.com/padi-courses/beginners/padi-scuba-diver.html)\n"
        "🔹 [PADI Open Water Diver - 8 990 THB](https://www.scubabirds.com/padi-courses/beginners/padi-open-water-diver.html)\n"
        "🔹 [Advance Open Water Diver – 8 500 THB](https://www.scubabirds.com/padi-courses/for-certified-divers/padi-advanced-open-water-diver.html)\n"
        "🔹 [Rescue Diver – 8 500 THB](https://www.scubabirds.com/padi-courses/for-certified-divers/padi-rescue-diver.html)\n"
        "🔹 [Fun Diving – от 1 400 THB](https://www.scubabirds.com/ko-tao/fun-diving-packages.html)\n\n"
        "📌 Более детально с нашими ценами погружений вы можете ознакомиться [на сайте](https://www.scubabirds.com/)."
    )
    await message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)

# Отправка документов
@router.message(lambda message: message.text == "📂 Получить документы")
async def send_documents(message: types.Message):
    document_path = os.path.join(os.getcwd(), "medical_form.pdf")  # Подгружаем файл из текущей директории
    
    if os.path.exists(document_path):
        with open(document_path, "rb") as doc:
            await message.answer_document(doc, caption="📎 Вот ваш документ!")
    else:
        await message.answer("❌ Ошибка: Файл *medical_form.pdf* не найден.\nПроверьте наличие файла в папке с ботом.", parse_mode="Markdown")

# Отправка ссылки на оплату
@router.message(lambda message: message.text == "💳 Оплатить")
async def payment_link(message: types.Message):
    text = "💳 *Оплатить можно по ссылке:*\n\n[Оплата](https://wise.com/pay/business/scubabirdscoltd)"
    await message.answer(text, parse_mode="Markdown")

# Функция для запуска бота
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

# Запуск бота через asyncio
if __name__ == "__main__":
    asyncio.run(main())
