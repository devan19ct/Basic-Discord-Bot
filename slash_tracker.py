import os
import json
from datetime import datetime

TRACKER_FILE = "slash_tracker.json"

def update_slash_usage():
    with open(TRACKER_FILE, "w") as f:
        json.dump({"last_used": datetime.utcnow().isoformat()}, f)

def get_last_slash_usage():
    if not os.path.exists(TRACKER_FILE):
        return None
    with open(TRACKER_FILE, "r") as f:
        data = json.load(f)
        return datetime.fromisoformat(data["last_used"])
