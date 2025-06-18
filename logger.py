import json
import os
from datetime import datetime

LOG_FILE = "dialog_log.json"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump({}, f)

def log_message(user_id: str, question: str, answer: str):
    with open(LOG_FILE, "r") as f:
        log = json.load(f)

    if user_id not in log:
        log[user_id] = []

    log[user_id].append({
        "time": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer
    })

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)