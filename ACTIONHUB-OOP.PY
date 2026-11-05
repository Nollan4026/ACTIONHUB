import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os


FILE_NAME = "tasks.json"


# ==========================================
# TASK CLASS
# ==========================================

class Task:

    def __init__(self, task, staff, priority, status="Pending"):

        self.task = task
        self.staff = staff
        self.priority = priority
        self.status = status

    # Convert Task object into dictionary
    def to_dict(self):

        return {
            "task": self.task,
            "staff": self.staff,
            "priority": self.priority,
            "status": self.status
        }

    # Convert dictionary into Task object
    @classmethod
    def from_dict(cls, data):

        return cls(
            data["task"],
            data["staff"],
            data["priority"],
            data["status"]
        )

    # Update task status
    def update_status(self, new_status):

        self.status = new_status

    # Display Task object
    def __str__(self):

        return (
            f"{self.task} - {self.staff} - "
            f"{self.priority} - {self.status}"
        )


# ==========================================
# ACTIONHUB APPLICATION CLASS
# ==========================================

class ActionHub:

    def __init__(self, root):

        self.root = root

        self.root.title("ActionHub - Bank Branch Task Tracker")
        self.root.geometry("900x650")
        self.root.configure(bg="#f4f6f8")

        # Load Task objects
        self.tasks = self.load_tasks()

        # Create application interface
        self.create_window()
        self.create_dashboard()
        self.create_task_table()
        self.create_buttons()

        # Display tasks and dashboard counts
        self.refresh_table()
        self.update_dashboard()

    # ======================================
    # LOAD TASKS
    # ======================================

    def load_tasks(self):

        if os.path.exists(FILE_NAME):

            try:

                with open(FILE_NAME, "r") as file:

                    tasks_data = json.load(file)

                return [
                    Task.from_dict(data)
                    for data in tasks_data
                ]

            except (json.JSONDecodeError, OSError, KeyError, TypeError):

                messagebox.showerror(
                    "Error",
                    "Unable to load tasks."
                )

                return []

        return []

    # ======================================
    # SAVE TASKS
    # ======================================

    def save_tasks(self):

        try:

            tasks_data = [
                task.to_dict()
                for task in self.tasks
            ]

            with open(FILE_NAME, "w") as file:

                json.dump(
                    tasks_data,
                    file,
                    indent=4
                )

        except OSError:

            messagebox.showerror(
                "Error",
                "Unable to save tasks."
            )

    # ======================================
    # CREATE MAIN WINDOW
    # ======================================

    def create_window(self):

        heading = tk.Label(
            self.root,
            text="ACTIONHUB",
            font=("Arial", 24, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        )

        heading.pack(pady=15)

        subtitle = tk.Label(
            self.root,
            text="BANK BRANCH TASK TRACKER",
            font=("Arial", 12),
            bg="#f4f6f8",
            fg="#64748b"
        )

        subtitle.pack()

    # ======================================
    # CREATE DASHBOARD
    # ======================================

    def create_dashboard(self):

        self.dashboard_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        self.dashboard_frame.pack(pady=20)

        self.total_label = self.create_counter(
            "Total Tasks", 0, 0
        )

        self.pending_label = self.create_counter(
            "Pending Tasks", 0, 1
        )

        self.completed_label = self.create_counter(
            "Completed Tasks", 1, 0
        )

        self.high_priority_label = self.create_counter(
            "High Priority", 1, 1
        )

    def create_counter(self, title, value, column):

        frame = tk.Frame(
            self.dashboard_frame,
            bg="white",
            padx=25,
            pady=10
        )

        frame.grid(
            row=0 if column < 2 else 1,
            column=column % 2,
            padx=10,
            pady=5
        )

        label = tk.Label(
            frame,
            text=f"{title}: {value}",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#1f2937"
        )

        label.pack()

        return label

    # ======================================
    # UPDATE DASHBOARD
    # ======================================

    def update_dashboard(self):

        total = len(self.tasks)

        pending = 0
        completed = 0
        high_priority = 0

        for task in self.tasks:

            if task.status == "Pending":
                pending += 1

            if task.status == "Completed":
                completed += 1

            if task.priority == "High":
                high_priority += 1

        self.total_label.config(
            text=f"Total Tasks: {total}"
        )

        self.pending_label.config(
            text=f"Pending Tasks: {pending}"
        )

        self.completed_label.config(
            text=f"Completed Tasks: {completed}"
        )

        self.high_priority_label.config(
            text=f"High Priority: {high_priority}"
        )

    # ======================================
    # CREATE TASK TABLE
    # ======================================

    def create_task_table(self):

        table_frame = tk.Frame(self.root)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "Task",
            "Staff",
            "Priority",
            "Status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=180
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ======================================
    # CREATE BUTTONS
    # ======================================

    def create_buttons(self):

        button_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        button_frame.pack(pady=15)

        buttons = [
            ("Add Task", self.add_task),
            ("View Tasks", self.view_tasks),
            ("Update Status", self.update_status),
            ("Delete Task", self.delete_task),
            ("Search", self.search_tasks),
            ("Exit", self.root.destroy)
        ]

        for text, command in buttons:

            tk.Button(
                button_frame,
                text=text,
                command=command,
                width=15,
                font=("Arial", 10, "bold")
            ).pack(
                side="left",
                padx=5
            )

    # ======================================
    # ADD TASK
    # ======================================

    def add_task(self):

        window = tk.Toplevel(self.root)

        window.title("Add Task")
        window.geometry("350x350")

        tk.Label(
            window,
            text="Add New Task",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Label(window, text="Task Name").pack()

        task_entry = tk.Entry(
            window,
            width=30
        )

        task_entry.pack(pady=5)

        tk.Label(window, text="Staff Name").pack()

        staff_entry = tk.Entry(
            window,
            width=30
        )

        staff_entry.pack(pady=5)

        tk.Label(window, text="Priority").pack()

        priority_box = ttk.Combobox(
            window,
            values=["High", "Medium", "Low"],
            state="readonly"
        )

        priority_box.set("Medium")
        priority_box.pack(pady=5)

        def save_new_task():

            task_name = task_entry.get().strip()
            staff_name = staff_entry.get().strip()
            priority = priority_box.get()

            if not task_name or not staff_name:

                messagebox.showwarning(
                    "Warning",
                    "Please enter task and staff name."
                )

                return

            # Create Task object
            task = Task(
                task_name,
                staff_name,
                priority,
                "Pending"
            )

            # Add object to list
            self.tasks.append(task)

            # Save and refresh
            self.save_tasks()
            self.refresh_table()
            self.update_dashboard()

            window.destroy()

            messagebox.showinfo(
                "Success",
                "Task added successfully."
            )

        tk.Button(
            window,
            text="Save Task",
            command=save_new_task,
            bg="lightgreen",
            font=("Arial", 11, "bold"),
            width=20
        ).pack(pady=20)

    # ======================================
    # VIEW TASKS
    # ======================================

    def view_tasks(self):

        self.refresh_table()

    # ======================================
    # REFRESH TASK TABLE
    # ======================================

    def refresh_table(self, filtered_tasks=None):

        for item in self.table.get_children():

            self.table.delete(item)

        if filtered_tasks is None:

            filtered_tasks = self.tasks

        for index, task in enumerate(self.tasks):

            if task not in filtered_tasks:
                continue

            self.table.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    task.task,
                    task.staff,
                    task.priority,
                    task.status
                )
            )

    # ======================================
    # UPDATE TASK STATUS
    # ======================================

    def update_status(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a task."
            )

            return

        index = int(selected[0])

        task = self.tasks[index]

        new_status = simpledialog.askstring(
            "Update Status",
            "Enter status (Pending or Completed):",
            initialvalue=task.status,
            parent=self.root
        )

        if new_status is None:
            return

        new_status = new_status.strip().title()

        if new_status not in ["Pending", "Completed"]:

            messagebox.showwarning(
                "Invalid Status",
                "Please enter Pending or Completed."
            )

            return

        # Update Task object
        task.update_status(new_status)

        self.save_tasks()
        self.refresh_table()
        self.update_dashboard()

    # ======================================
    # DELETE TASK
    # ======================================

    def delete_task(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a task."
            )

            return

        index = int(selected[0])

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this task?"
        )

        if confirm:

            # Remove Task object
            self.tasks.pop(index)

            self.save_tasks()
            self.refresh_table()
            self.update_dashboard()

    # ======================================
    # SEARCH TASKS
    # ======================================

    def search_tasks(self):

        search_text = simpledialog.askstring(
            "Search Tasks",
            "Enter task, staff, priority or status:",
            parent=self.root
        )

        if search_text is None:
            return

        search_text = search_text.strip().lower()

        matching_tasks = []

        for task in self.tasks:

            if (
                search_text in task.task.lower()
                or search_text in task.staff.lower()
                or search_text in task.priority.lower()
                or search_text in task.status.lower()
            ):

                matching_tasks.append(task)

        self.refresh_table(matching_tasks)

        if not matching_tasks:

            messagebox.showinfo(
                "Search",
                "No matching tasks found."
            )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ActionHub(root)

    root.mainloop()