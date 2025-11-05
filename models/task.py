import json
import os
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'tasks.json')


class TaskModel:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as file:
                try:
                    self.tasks = json.load(file)
                except json.JSONDecodeError:
                    self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(TASKS_FILE, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title, priority, deadline):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "priority": priority,
            "deadline": deadline,
            "progress": 0,
            "status": "Pending"
        }
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        for i, t in enumerate(self.tasks):
            t["id"] = i + 1
        self.save_tasks()

    def update_progress(self, task_id, progress):
        for task in self.tasks:
            if task["id"] == task_id:
                task["progress"] = progress
                if progress >= 100:
                    task["progress"] = 100
                    task["status"] = "Completed"
                elif progress > 0:
                    task["status"] = "In Progress"
                else:
                    task["status"] = "Pending"
        self.save_tasks()
