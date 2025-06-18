from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GPT_API_KEY = os.getenv("GPT_API_KEY")
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")