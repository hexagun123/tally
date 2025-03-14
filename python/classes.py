import tkinter as tk
import json
import randomTask
from datetime import datetime

# Task class to represent each task with its attributes
class Task:
    def __init__(self, name, streak, updated, last_updated):
        self.name = name
        self.streak = streak
        self.updated = updated
        self.last_updated = last_updated

    def __str__(self):
        return f"Task(name={self.name}, streak={self.streak}, updated={self.updated}, last_updated={self.last_updated})"

# Page class to handle the display of tasks
class Page:
    def __init__(self, tasks):
        self.tasks = tasks

    # Display tasks in the root window
    def display(self, root):
        for i, task in enumerate(self.tasks):
            tk.Label(root, text=task.name).grid(row=i+2, column=0, padx=5, pady=2, sticky="ew")
            tk.Label(root, text=f"Streak: {task.streak}").grid(row=i+2, column=1, padx=5, pady=2, sticky="ew")
            var = tk.BooleanVar(value=task.updated)
            checkbox = tk.Checkbutton(root, variable=var, command=lambda t=task, v=var: self.update_task_status(t, v))
            checkbox.grid(row=i+2, column=2, padx=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=0)

    # Update the status of a task
    def update_task_status(self, task, var):
        task.updated = var.get()

# Screen class to initialize the main window and load tasks
class Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Status Screen")
        self.root.geometry("1024x768")
        self.tasks = self.load_tasks()
        self.page = Page(self.tasks)
        self.menu = Menu(self.root, self.page)

    # Load tasks from JSON file
    def load_tasks(self):
        try:
            with open('pstatus.json', 'r') as file:
                data = json.load(file)
                return [Task(task['name'], task['streak'], task['updated'], task['last_updated']) for task in data]
        except FileNotFoundError:
            with open('pstatus.json', 'w') as file:
                json.dump([], file, indent=4)
            return []

    # Run the main loop
    def run(self):
        self.root.mainloop()

# Menu class to handle the main menu and task operations
class Menu:
    def __init__(self, root, page):
        self.root = root
        self.page = page
        self.create_main_menu()

    # Create the main menu
    def create_main_menu(self):
        self.label = tk.Label(self.root, text="Task Status Screen")
        self.label.place(relx=0.35, rely=0.1, relwidth=0.3)

        self.button = tk.Button(self.root, text="Tasks", command=self.display_tasks)
        self.button.place(relx=0.35, rely=0.2, relwidth=0.3)

        self.button1 = tk.Button(self.root, text="Random Task", command=self.random_task)
        self.button1.place(relx=0.35, rely=0.3, relwidth=0.3)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_tasks)
        self.save_button.place(relx=0.35, rely=0.4, relwidth=0.3)

    def random_task(self):
        randomTask.RandomiserApp(self.page.tasks)

    # Check and update the streak of a task
    def streak_check(self, task):
        today = datetime.now().strftime('%Y-%m-%d')
        if task.last_updated != today:
            if task.updated:
                task.streak += 1
                task.updated = False
            else:
                task.streak = 0
            task.last_updated = today

    # Display tasks and update their streaks
    def display_tasks(self):
        self.clear_widgets()
        for task in self.page.tasks:
            self.streak_check(task)
        self.save_tasks()

        return_button = tk.Button(self.root, text="Return", command=self.return_to_main)
        return_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        new_task_button = tk.Button(self.root, text="Enter New Tasks", command=self.enter_new_tasks)
        new_task_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.page.display(self.root)

    # Enter new tasks
    def enter_new_tasks(self):
        self.clear_widgets()

        return_button = tk.Button(self.root, text="Return", command=self.return_to_main)
        return_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        name_label = tk.Label(self.root, text="Task Name:")
        name_label.grid(row=1, column=0, padx=10, pady=5)
        name_entry = tk.Entry(self.root)
        name_entry.grid(row=1, column=1, padx=10, pady=5)

        def save_new_task():
            name = name_entry.get()
            if name:
                new_task = Task(name, 0, False, datetime.now().strftime('%Y-%m-%d'))
                self.page.tasks.append(new_task)
                self.save_tasks()
                self.display_tasks()

        enter_button = tk.Button(self.root, text="Enter", command=save_new_task)
        enter_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    # Return to the main menu
    def return_to_main(self):
        self.clear_widgets()
        self.create_main_menu()

    # Save tasks to JSON file
    def save_tasks(self):
        tasks_data = [{'name': task.name, 'streak': task.streak, 'updated': task.updated, 'last_updated': task.last_updated} for task in self.page.tasks]
        with open('pstatus.json', 'w') as file:
            json.dump(tasks_data, file, indent=4)

    # Clear all widgets from the root window
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    screen = Screen()
    screen.run()