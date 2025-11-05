import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.task import TaskModel
from views.dashboard import DashboardView


class GoalTrackrApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GoalTrackr - Smart Productivity Manager")
        self.geometry("950x650")
        self.configure(bg="#121212")

        self.task_model = TaskModel()
        self.dashboard = DashboardView(self, self.task_model)
        self.dashboard.pack(fill="both", expand=True)

        self.create_add_task_button()

    def create_add_task_button(self):
        add_btn = tk.Button(
            self,
            text="+ Add Task",
            bg="#1DB954",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            command=self.open_add_task_window
        )
        add_btn.place(x=20, y=20, width=120, height=40)

    def open_add_task_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add New Task")
        add_window.geometry("400x320")
        add_window.configure(bg="#1E1E1E")

        tk.Label(add_window, text="Task Title:", bg="#1E1E1E", fg="white", font=("Segoe UI", 10)).pack(pady=10)
        title_entry = tk.Entry(add_window, font=("Segoe UI", 10), width=30)
        title_entry.pack()

        tk.Label(add_window, text="Priority:", bg="#1E1E1E", fg="white", font=("Segoe UI", 10)).pack(pady=10)
        priority_var = tk.StringVar(value="Medium")
        ttk.Combobox(add_window, textvariable=priority_var, values=["High", "Medium", "Low"], width=28).pack()

        tk.Label(add_window, text="Deadline (YYYY-MM-DD):", bg="#1E1E1E", fg="white", font=("Segoe UI", 10)).pack(pady=10)
        deadline_entry = tk.Entry(add_window, font=("Segoe UI", 10), width=30)
        deadline_entry.pack()

        def save_task():
            title = title_entry.get()
            priority = priority_var.get()
            deadline = deadline_entry.get()
            if not title.strip():
                messagebox.showerror("Error", "Task title cannot be empty!")
                return
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return

            self.task_model.add_task(title, priority, deadline)
            self.dashboard.refresh_table()
            add_window.destroy()

        tk.Button(add_window, text="Save", command=save_task, bg="#1DB954", fg="white", font=("Segoe UI", 10)).pack(pady=20)
