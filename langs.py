import json
import os

LANG_FILE = "lang_settings.json"

TEXTS = {
    "welcome": {
        "en": "👋 Hello! I'm your GPT assistant. Send me a question and I'll reply. You have 3 free messages.",
        "ru": "👋 Привет! Я GPT-бот. Напиши мне вопрос, и я постараюсь ответить. У тебя 3 бесплатных сообщения."
    },
    "limit": {
        "en": "❌ You used all your free messages. Please pay to continue.",
        "ru": "❌ Вы использовали лимит бесплатных сообщений. Пожалуйста, оплатите, чтобы продолжить."
    },
    "pay_button": {
        "en": "💳 Pay",
        "ru": "💳 Оплатить"
    },
    "thinking": {
        "en": "✍️ Thinking...",
        "ru": "✍️ Думаю..."
    },
    "error": {
        "en": "❌ GPT request failed.",
        "ru": "❌ Ошибка при запросе к GPT."
    }
    ,
    "reset_limit": {
        "en": "Reset limit",
        "ru": "Сбросить лимит"
    },
    "payment_description": {
        "en": "Get full access to the assistant without limits.",
        "ru": "Получите полный доступ к ассистенту без ограничений."
    },
    "payment_success": {
        "en": "✅ Payment successful. Limit reset.",
        "ru": "✅ Оплата прошла успешно. Лимит сброшен."
    }

    ,
    "ask": {
        "en": "Ask a question",
        "ru": "Задать вопрос"
    },
    "ask_prompt": {
        "en": "Please enter your question:",
        "ru": "Пожалуйста, введите ваш вопрос:"
    },
    "change_lang": {
        "en": "Change language",
        "ru": "Сменить язык"
    }

}

if not os.path.exists(LANG_FILE):
    with open(LANG_FILE, "w") as f:
        json.dump({}, f)

def get_lang(user_id: str) -> str:
    with open(LANG_FILE, "r") as f:
        langs = json.load(f)
    return langs.get(user_id, "ru")

def set_lang(user_id: str, lang: str):
    with open(LANG_FILE, "r") as f:
        langs = json.load(f)
    langs[user_id] = lang
    with open(LANG_FILE, "w") as f:
        json.dump(langs, f)

def get_text(key: str, lang: str) -> str:
    return TEXTS.get(key, {}).get(lang, "")