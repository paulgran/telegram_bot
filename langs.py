import json, os
LANG_FILE = "lang_settings.json"
TEXTS = {
    "welcome": {"en": "👋 Hello! I'm your GPT assistant. You have 3 free messages.",
                "ru": "👋 Привет! Я GPT-бот. У тебя 3 бесплатных сообщения."},
    "ask": {"en": "Ask a question", "ru": "Задать вопрос"},
    "ask_prompt": {"en": "Please enter your question:", "ru": "Пожалуйста, введите ваш вопрос:"},
    "change_lang": {"en": "Change language", "ru": "Сменить язык"},
    "reset_limit": {"en": "Reset limit", "ru": "Сбросить лимит"},
    "pay_button": {"en": "💳 Pay", "ru": "💳 Оплатить"},
    "manual_payment": {"en": "To continue, please pay via the link below and wait for manual approval.",
                       "ru": "Чтобы продолжить, оплатите по ссылке ниже и дождитесь ручного подтверждения."},
    "thinking": {"en": "✍️ Thinking...", "ru": "✍️ Думаю..."},
    "error": {"en": "❌ GPT request failed.", "ru": "❌ Ошибка при запросе к GPT."}
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