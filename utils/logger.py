import os
from datetime import datetime

def log_event(message):
    os.makedirs("logs", exist_ok=True)
    with open(os.path.join("logs", "app_log.txt"), "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")
