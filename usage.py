import json, os
USAGE_FILE = "usage_log.json"
LIMIT = 3
if not os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, "w") as f:
        json.dump({}, f)
def check_and_update_usage(user_id: str) -> bool:
    with open(USAGE_FILE, "r") as f:
        usage = json.load(f)
    count = usage.get(user_id, 0)
    if count >= LIMIT:
        return False
    usage[user_id] = count + 1
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f)
    return True
def reset_usage(user_id: str):
    with open(USAGE_FILE, "r") as f:
        usage = json.load(f)
    usage[user_id] = 0
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f)