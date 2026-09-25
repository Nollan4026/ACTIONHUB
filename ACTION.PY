import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


# =========================
# FILE STORAGE
# =========================

FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []


tasks = load_tasks()


def save_tasks():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        messagebox.showerror("Error", "Unable to save tasks.")


# =========================
# DASHBOARD
# =========================

def update_dashboard():

    total = len(tasks)

    pending = sum(
        1 for task in tasks
        if task.get("status") == "Pending"
    )

    completed = sum(
        1 for task in tasks
        if task.get("status") == "Completed"
    )

    high_priority = sum(
        1 for task in tasks
        if task.get("priority") == "High"
    )

    total_label.config(
        text=f"Total Tasks: {total}"
    )

    pending_label.config(
        text=f"Pending Tasks: {pending}"
    )

    completed_label.config(
        text=f"Completed Tasks: {completed}"
    )

    high_priority_label.config(
        text=f"High Priority: {high_priority}"
    )


# =========================
# ADD TASK
# =========================

def add_task():

    task_window = tk.Toplevel(root)
    task_window.title("Add Task")
    task_window.geometry("400x400")
    task_window.configure(bg="#f4f6f8")

    tk.Label(
        task_window,
        text="ADD NEW TASK",
        font=("Arial", 16, "bold"),
        bg="#f4f6f8"
    ).pack(pady=15)

    tk.Label(
        task_window,
        text="Task:",
        bg="#f4f6f8"
    ).pack()

    task_entry = tk.Entry(
        task_window,
        width=35
    )
    task_entry.pack(pady=5)

    tk.Label(
        task_window,
        text="Staff Name:",
        bg="#f4f6f8"
    ).pack()

    staff_entry = tk.Entry(
        task_window,
        width=35
    )
    staff_entry.pack(pady=5)

    tk.Label(
        task_window,
        text="Priority:",
        bg="#f4f6f8"
    ).pack()

    priority_combo = ttk.Combobox(
        task_window,
        values=["High", "Medium", "Low"],
        state="readonly",
        width=32
    )
    priority_combo.pack(pady=5)
    priority_combo.set("Medium")

    def save_new_task():

        task_text = task_entry.get().strip()
        staff_name = staff_entry.get().strip()
        priority = priority_combo.get()

        if task_text == "" or staff_name == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter the task and staff name."
            )
            return

        new_task = {
            "task": task_text,
            "staff": staff_name,
            "priority": priority,
            "status": "Pending"
        }

        tasks.append(new_task)

        save_tasks()
        update_dashboard()

        messagebox.showinfo(
            "Success",
            "Task added successfully."
        )

        task_window.destroy()

    tk.Button(
        task_window,
        text="Save Task",
        width=20,
        command=save_new_task
    ).pack(pady=20)


# =========================
# VIEW TASKS
# =========================

def view_tasks():

    view_window = tk.Toplevel(root)
    view_window.title("View Tasks")
    view_window.geometry("800x500")
    view_window.configure(bg="#f4f6f8")

    tk.Label(
        view_window,
        text="ACTIONHUB TASKS",
        font=("Arial", 18, "bold"),
        bg="#f4f6f8"
    ).pack(pady=15)

    table_frame = tk.Frame(
        view_window,
        bg="#f4f6f8"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
        "No.",
        "Task",
        "Staff",
        "Priority",
        "Status"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    table.heading("No.", text="No.")
    table.heading("Task", text="Task")
    table.heading("Staff", text="Staff")
    table.heading("Priority", text="Priority")
    table.heading("Status", text="Status")

    table.column("No.", width=50)
    table.column("Task", width=300)
    table.column("Staff", width=150)
    table.column("Priority", width=100)
    table.column("Status", width=100)

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=scrollbar.set
    )

    table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    for index, task in enumerate(tasks, start=1):

        table.insert(
            "",
            "end",
            values=(
                index,
                task.get("task", ""),
                task.get("staff", ""),
                task.get("priority", ""),
                task.get("status", "")
            )
        )


# =========================
# UPDATE STATUS
# =========================

def update_status():

    status_window = tk.Toplevel(root)
    status_window.title("Update Status")
    status_window.geometry("400x300")
    status_window.configure(bg="#f4f6f8")

    tk.Label(
        status_window,
        text="UPDATE TASK STATUS",
        font=("Arial", 16, "bold"),
        bg="#f4f6f8"
    ).pack(pady=15)

    tk.Label(
        status_window,
        text="Select Task:",
        bg="#f4f6f8"
    ).pack()

    task_names = [
        f"{index + 1}. {task.get('task', '')}"
        for index, task in enumerate(tasks)
    ]

    task_combo = ttk.Combobox(
        status_window,
        values=task_names,
        state="readonly",
        width=35
    )

    task_combo.pack(pady=10)

    tk.Label(
        status_window,
        text="New Status:",
        bg="#f4f6f8"
    ).pack()

    status_combo = ttk.Combobox(
        status_window,
        values=["Pending", "Completed"],
        state="readonly",
        width=35
    )

    status_combo.pack(pady=10)
    status_combo.set("Completed")

    def save_status():

        selected = task_combo.current()

        if selected == -1:
            messagebox.showwarning(
                "No Task",
                "Please select a task."
            )
            return

        new_status = status_combo.get()

        tasks[selected]["status"] = new_status

        save_tasks()
        update_dashboard()

        messagebox.showinfo(
            "Success",
            "Task status updated successfully."
        )

        status_window.destroy()

    tk.Button(
        status_window,
        text="Update Status",
        width=20,
        command=save_status
    ).pack(pady=20)


# =========================
# DELETE TASK
# =========================

def delete_task():

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Task")
    delete_window.geometry("400x300")
    delete_window.configure(bg="#f4f6f8")

    tk.Label(
        delete_window,
        text="DELETE TASK",
        font=("Arial", 16, "bold"),
        bg="#f4f6f8"
    ).pack(pady=15)

    task_names = [
        f"{index + 1}. {task.get('task', '')}"
        for index, task in enumerate(tasks)
    ]

    task_combo = ttk.Combobox(
        delete_window,
        values=task_names,
        state="readonly",
        width=35
    )

    task_combo.pack(pady=20)

    def confirm_delete():

        selected = task_combo.current()

        if selected == -1:
            messagebox.showwarning(
                "No Task",
                "Please select a task."
            )
            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this task?"
        )

        if answer:

            tasks.pop(selected)

            save_tasks()
            update_dashboard()

            messagebox.showinfo(
                "Success",
                "Task deleted successfully."
            )

            delete_window.destroy()

    tk.Button(
        delete_window,
        text="Delete Task",
        width=20,
        command=confirm_delete
    ).pack(pady=10)


# =========================
# SEARCH TASKS
# =========================

def search_tasks():

    search_window = tk.Toplevel(root)
    search_window.title("Search Tasks")
    search_window.geometry("700x450")
    search_window.configure(bg="#f4f6f8")

    tk.Label(
        search_window,
        text="SEARCH ACTIONHUB",
        font=("Arial", 18, "bold"),
        bg="#f4f6f8"
    ).pack(pady=15)

    search_entry = tk.Entry(
        search_window,
        width=40
    )

    search_entry.pack(pady=10)

    table_frame = tk.Frame(
        search_window,
        bg="#f4f6f8"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
        "No.",
        "Task",
        "Staff",
        "Priority",
        "Status"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(
            column,
            text=column
        )

    table.pack(
        fill="both",
        expand=True
    )

    def perform_search():

        for item in table.get_children():
            table.delete(item)

        search_text = search_entry.get().lower()

        for index, task in enumerate(tasks, start=1):

            if (
                search_text in task.get("task", "").lower()
                or search_text in task.get("staff", "").lower()
                or search_text in task.get("priority", "").lower()
                or search_text in task.get("status", "").lower()
            ):

                table.insert(
                    "",
                    "end",
                    values=(
                        index,
                        task.get("task", ""),
                        task.get("staff", ""),
                        task.get("priority", ""),
                        task.get("status", "")
                    )
                )

    tk.Button(
        search_window,
        text="Search",
        width=20,
        command=perform_search
    ).pack(pady=10)


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("ActionHub")
root.geometry("500x650")

root.configure(bg="#f4f6f8")


# =========================
# MAIN TITLE
# =========================

title_label = tk.Label(
    root,
    text="ACTIONHUB",
    bg="#f4f6f8",
    font=("Arial", 18, "bold")
)

title_label.pack(pady=20)


# =========================
# DASHBOARD FRAME
# =========================

dashboard_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

dashboard_frame.pack(pady=20)


# =========================
# DASHBOARD LABELS
# =========================

total_label = tk.Label(
    dashboard_frame,
    text="Total Tasks: 0",
    bg="#f4f6f8",
    font=("Arial", 12, "bold")
)

total_label.pack(pady=5)


pending_label = tk.Label(
    dashboard_frame,
    text="Pending Tasks: 0",
    bg="#f4f6f8",
    font=("Arial", 12, "bold")
)

pending_label.pack(pady=5)


completed_label = tk.Label(
    dashboard_frame,
    text="Completed Tasks: 0",
    bg="#f4f6f8",
    font=("Arial", 12, "bold")
)

completed_label.pack(pady=5)


high_priority_label = tk.Label(
    dashboard_frame,
    text="High Priority: 0",
    bg="#f4f6f8",
    font=("Arial", 12, "bold")
)

high_priority_label.pack(pady=5)


# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

button_frame.pack(pady=25)


# =========================
# MAIN BUTTONS
# =========================

add_button = tk.Button(
    button_frame,
    text="Add Task",
    width=25,
    command=add_task
)

add_button.pack(pady=5)


view_button = tk.Button(
    button_frame,
    text="View Tasks",
    width=25,
    command=view_tasks
)

view_button.pack(pady=5)


update_button = tk.Button(
    button_frame,
    text="Update Status",
    width=25,
    command=update_status
)

update_button.pack(pady=5)


delete_button = tk.Button(
    button_frame,
    text="Delete Task",
    width=25,
    command=delete_task
)

delete_button.pack(pady=5)


search_button = tk.Button(
    button_frame,
    text="Search Tasks",
    width=25,
    command=search_tasks
)

search_button.pack(pady=5)


exit_button = tk.Button(
    button_frame,
    text="Exit",
    width=25,
    command=root.destroy
)

exit_button.pack(pady=5)


# =========================
# START APPLICATION
# =========================

update_dashboard()

root.mainloop()
