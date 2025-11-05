import threading
import time
from datetime import datetime, timedelta
from models.task import get_all_tasks
import tkinter as tk
from tkinter import messagebox


def check_upcoming_deadlines():
    while True:
        tasks = get_all_tasks()
        now = datetime.now()
        upcoming = []

        for t in tasks:
            _, title, _, due_date, completed = t
            if completed == 0:
                try:
                    due = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
                    if now <= due <= now + timedelta(minutes=30):
                        upcoming.append(title)
                except:
                    continue

        if upcoming:
            show_popup(upcoming)

        time.sleep(60)  # check every minute


def show_popup(tasks):
    root = tk.Tk()
    root.withdraw()  # hide root window
    msg = "\n".join(tasks)
    messagebox.showinfo("🔔 Upcoming Tasks", f"The following tasks are due soon:\n\n{msg}")
    root.destroy()


def start_reminder_thread():
    thread = threading.Thread(target=check_upcoming_deadlines, daemon=True)
    thread.start()
