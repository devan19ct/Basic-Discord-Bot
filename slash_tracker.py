import os
import json
from datetime import datetime
from pytz import timezone

TRACKER_FILE = "slash_tracker.json"

def update_slash_usage():
    ist = timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    print(f"[Slash used] {now_ist.isoformat()}")

    with open(TRACKER_FILE, "w") as f:
        json.dump({"last_used": now_ist.isoformat()}, f)
        print(f"[File written] {TRACKER_FILE}")

def get_last_slash_usage():
    if not os.path.exists(TRACKER_FILE):
        return None
    with open(TRACKER_FILE, "r") as f:
        data = json.load(f)
        ist = timezone("Asia/Kolkata")
        return datetime.fromisoformat(data["last_used"]).astimezone(ist)

