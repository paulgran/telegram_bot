import json
import os
from datetime import datetime

STATS_FILE = "user_stats.json"

if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, "w") as f:
        json.dump({}, f)

def log_user(user_id: str, username: str):
    with open(STATS_FILE, "r") as f:
        stats = json.load(f)

    stats[user_id] = {
        "username": username,
        "joined": datetime.utcnow().isoformat()
    }

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)def get_all_users():
    with open(STATS_FILE, "r") as f:
        stats = json.load(f)
    return stats