import tkinter as tk
from tkinter import ttk, messagebox


class DashboardView(tk.Frame):
    def __init__(self, parent, task_model):
        super().__init__(parent, bg="#121212")
        self.task_model = task_model
        self.create_ui()

    def create_ui(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1E1E1E",
                        fieldbackground="#1E1E1E",
                        foreground="white",
                        rowheight=35)
        style.configure("Treeview.Heading",
                        background="#1DB954",
                        foreground="black",
                        font=("Segoe UI", 10, "bold"))

        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Title", "Priority", "Deadline", "Progress", "Status"),
            show="headings",
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=(80, 20))
        self.create_buttons()
        self.refresh_table()

    def create_buttons(self):
        button_frame = tk.Frame(self, bg="#121212")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Update Progress", bg="#0078D7", fg="white",
                  font=("Segoe UI", 10), relief="flat", command=self.open_update_progress).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Delete Task", bg="#E81123", fg="white",
                  font=("Segoe UI", 10), relief="flat", command=self.delete_task).grid(row=0, column=1, padx=10)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for task in self.task_model.tasks:
            progress_bar = f"{task['progress']}%"
            display_title = task["title"]
            if task["progress"] == 100:
                display_title = f"✔ {display_title} (Done)"
            self.tree.insert("", "end", values=(
                task["id"],
                display_title,
                task["priority"],
                task["deadline"],
                progress_bar,
                task["status"]
            ))

    def open_update_progress(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task first.")
            return

        task_id = int(self.tree.item(selected, "values")[0])
        update_window = tk.Toplevel(self)
        update_window.title("Update Progress")
        update_window.geometry("320x250")
        update_window.configure(bg="#1E1E1E")

        tk.Label(update_window, text="Set Progress (%):", bg="#1E1E1E", fg="white", font=("Segoe UI", 10)).pack(pady=10)

        progress_var = tk.IntVar(value=0)
        progress_value_label = tk.Label(update_window, text="0%", bg="#1E1E1E", fg="#1DB954", font=("Segoe UI", 11, "bold"))
        progress_value_label.pack()

        def on_slide(value):
            progress_value_label.config(text=f"{int(float(value))}%")

        progress_slider = ttk.Scale(update_window, from_=0, to=100, orient="horizontal",
                                    variable=progress_var, length=200, command=on_slide)
        progress_slider.pack(pady=10)

        def update():
            progress = int(progress_var.get())
            self.task_model.update_progress(task_id, progress)
            self.refresh_table()
            update_window.destroy()

        tk.Button(update_window, text="Update", command=update, bg="#1DB954", fg="white", font=("Segoe UI", 10)).pack(pady=20)

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return

        task_id = int(self.tree.item(selected, "values")[0])
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
        if confirm:
            self.task_model.delete_task(task_id)
            self.refresh_table()
