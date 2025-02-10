import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# Загружаем токен из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("\u274C Ошибка: TELEGRAM_BOT_TOKEN не загружен!")
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
        [KeyboardButton(text="\ud83d\udccb Наши услуги"), KeyboardButton(text="\ud83d\udcb0 Цены")],
        [KeyboardButton(text="\ud83d\udcc2 Получить документы"), KeyboardButton(text="\ud83d\udcb3 Оплатить")],
        [KeyboardButton(text="\ud83d\udce4 Свяжитесь с нами")]
    ],
    resize_keyboard=True
)

# Клавиатура для "Наши услуги"
services_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Услуга 1", callback_data="service_1")],
        [InlineKeyboardButton(text="Услуга 2", callback_data="service_2")],
        [InlineKeyboardButton(text="Услуга 3", callback_data="service_3")],
        [InlineKeyboardButton(text="Услуга 4", callback_data="service_4")],
        [InlineKeyboardButton(text="Услуга 5", callback_data="service_5")],
        [InlineKeyboardButton(text="Услуга 6", callback_data="service_6")],
        [InlineKeyboardButton(text="Услуга 7", callback_data="service_7")],
        [InlineKeyboardButton(text="Услуга 8", callback_data="service_8")],
    ]
)

# Клавиатура для "Цены"
prices_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Цена 1", callback_data="price_1")],
        [InlineKeyboardButton(text="Цена 2", callback_data="price_2")],
        [InlineKeyboardButton(text="Цена 3", callback_data="price_3")],
        [InlineKeyboardButton(text="Цена 4", callback_data="price_4")],
        [InlineKeyboardButton(text="Цена 5", callback_data="price_5")],
        [InlineKeyboardButton(text="Цена 6", callback_data="price_6")],
        [InlineKeyboardButton(text="Цена 7", callback_data="price_7")],
        [InlineKeyboardButton(text="Цена 8", callback_data="price_8")],
    ]
)

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добрый день! Мы рады приветствовать вас в нашем Дайв Центре Scuba Birds! Выберите нужный раздел:",
        reply_markup=main_keyboard
    )

# Обработчик кнопки "Наши услуги"
@router.message(lambda message: message.text == "\ud83d\udccb Наши услуги")
async def services_command(message: types.Message):
    await message.answer("Наши услуги:", reply_markup=services_keyboard)

# Обработчик кнопки "Цены"
@router.message(lambda message: message.text == "\ud83d\udcb0 Цены")
async def prices_command(message: types.Message):
    await message.answer("Наши цены:", reply_markup=prices_keyboard)

# Обработчик кнопки "Свяжитесь с нами"
@router.message(lambda message: message.text == "\ud83d\udce4 Свяжитесь с нами")
async def contact_command(message: types.Message):
    whatsapp_url = "https://wa.me/66990307571"
    await message.answer(
        "Нажмите на кнопку ниже, чтобы связаться с нами через WhatsApp:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Связаться в WhatsApp", url=whatsapp_url)]
            ]
        )
    )

# Обработчик кнопки "Получить документы"
@router.message(lambda message: message.text == "\ud83d\udcc2 Получить документы")
async def get_documents(message: types.Message):
    try:
        document_path = "example_document.pdf"  # Укажите путь к вашему документу
        await message.answer_document(open(document_path, "rb"))
    except Exception as e:
        await message.answer("Не удалось загрузить документы. Пожалуйста, попробуйте позже.")
        logging.error(f"Ошибка загрузки документов: {e}")

# Добавляем ссылку на сайт в основной раздел
@router.message(lambda message: message.text == "\ud83d\udcb3 Оплатить")
async def website_link(message: types.Message):
    await message.answer(
        "Посетите наш сайт для получения дополнительной информации:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Посетить сайт", url="https://scubabirds.com")]
            ]
        )
    )

# Запуск бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
