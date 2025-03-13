import requests
from bs4 import BeautifulSoup
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Токены
TELEGRAM_BOT_TOKEN = "your_telegram_token"
OPENAI_API_KEY = "your_openai_api_key"

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Функция для парсинга сайта
def get_info_from_scubabirds():
    url = "https://www.scubabirds.ru/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Извлекаем текст из главной страницы
        paragraphs = soup.find_all('p')  # Находим все теги <p>
        text_content = " ".join([p.get_text() for p in paragraphs])
        
        return text_content[:1000]  # Ограничиваем до 1000 символов, чтобы не перегружать GPT
    return "Ошибка при получении данных с сайта."

# Функция для запроса к ChatGPT
def ask_gpt(prompt):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Ты помощник, который отвечает на вопросы о дайвинге."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот Scuba Birds 🐠. Задавай вопросы о дайвинге!")

# Обработчик текстовых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    user_query = message.text
    website_data = get_info_from_scubabirds()
    
    gpt_prompt = f"Вот информация с сайта Scuba Birds: {website_data}. Теперь ответь на вопрос: {user_query}"
    gpt_response = ask_gpt(gpt_prompt)
    
    await message.reply(gpt_response)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)