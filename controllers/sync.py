import json
import os
import time

SYNC_FILE = os.path.join("data", "cloud_sync.json")

def sync_to_cloud(data):
    os.makedirs("data", exist_ok=True)
    with open(SYNC_FILE, "w") as f:
        json.dump(data, f, indent=4)
    time.sleep(1)
    return True

def sync_from_cloud():
    if os.path.exists(SYNC_FILE):
        with open(SYNC_FILE, "r") as f:
            return json.load(f)
    return []
