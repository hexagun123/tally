import tkinter as tk
import json
import randomTask
import stats
from datetime import datetime
import os

# Task class to represent each task with its attributes
class Task:
    def __init__(self, name, streak, updated, last_updated, attributes=None):
        self.name = name
        self.streak = streak
        self.updated = updated
        self.last_updated = last_updated
        self.attributes = attributes

    def __str__(self):
        return f"Task(name={self.name}, streak={self.streak}, updated={self.updated}, last_updated={self.last_updated}, attributes={self.attributes})"

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
                return [Task(task['name'], task['streak'], task['updated'], task['last_updated'], task["attributes"]) for task in data]
        except FileNotFoundError:
            with open('pstatus.json', 'w') as file:
                json.dump([], file, indent=4)
            return []

    # Run the main loop
    def run(self):
        self.root.mainloop()

"""
    A class to create and manage the main menu and task-related functionalities in a Tkinter application.
    Attributes:
    root : Tk
        The root window of the Tkinter application.
    page : Page
        The page object containing tasks and other related data.
    Methods:
    create_main_menu():
        Creates the main menu with buttons for various functionalities.
    stats_screen():
        Opens the stats screen.
    random_task():
        Opens the random task screen.
    streak_check(task):
        Checks and updates the streak of a given task.
    modify_task(name):
        Modifies an existing task and resets its streak.
    display_tasks():
        Displays the list of tasks and updates their streaks.
    enter_new_tasks():
        Allows the user to enter new tasks.
    return_to_main():
        Returns to the main menu.
    save_tasks():
        Saves the tasks to a JSON file and creates a backup.
    clear_widgets():
        Clears all widgets from the root window.
"""
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

        self.button2 = tk.Button(self.root, text="Stats screen", command=self.stats_screen)
        self.button2.place(relx=0.35, rely=0.4, relwidth=0.3)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_tasks)
        self.save_button.place(relx=0.35, rely=0.5, relwidth=0.3)

    def stats_screen(self):
        stats.StatusScreen()

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

    def modify_task(self,name):
        self.clear_widgets()

        return_button = tk.Button(self.root, text="Return", command=self.return_to_main)
        return_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        name_label = tk.Label(self.root, text="Warning: Modifying a task will reset its streak.")
        name_label.grid(row=1, column=0, padx=10, pady=5)
        name_label = tk.Label(self.root, text="Task Name:")
        name_label.grid(row=1, column=1, padx=10, pady=5)
        name_entry = tk.Entry(self.root)
        name_entry.insert(0, name)
        name_entry.grid(row=1, column=2, padx=10, pady=5)

        # Load stats from JSON file
        try:
            with open('stats.json', 'r') as file:
                stats_data = json.load(file)
        except FileNotFoundError:
            stats_data = []

        # Create a label for the checkbox table
        table_label = tk.Label(self.root, text="Tick all that apply:")
        table_label.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

        # Create checkboxes for each stat name
        check_vars = []
        if stats_data != []:
            for i, attribute in enumerate(stats_data["attributes"]):
                var = tk.BooleanVar()
                check_vars.append([attribute,var])
                checkbox = tk.Checkbutton(self.root, text=attribute, variable=var)
                checkbox.grid(row=4+i, column=0, padx=10, pady=2, columnspan=2)


        def modify_task():
            name = name_entry.get()
            x = []
            if name:
                for i in check_vars:
                    if i[1].get():
                        x.append(i[0])
                new_task = Task(name, 0, False, datetime.now().strftime('%Y-%m-%d'),x)
                self.page.tasks = [t for t in self.page.tasks if t.name != name]
                self.page.tasks.append(new_task)
                self.save_tasks()
                self.display_tasks()


        enter_button = tk.Button(self.root, text="Enter", command=modify_task)
        enter_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    # Display tasks and update their streaks
    def display_tasks(self):
        self.clear_widgets()
        for task in self.page.tasks:
            self.streak_check(task)
        self.save_tasks()

        return_button = tk.Button(self.root, text="Return", command=self.return_to_main)
        return_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        new_task_button = tk.Button(self.root, text="Enter New Tasks", command=self.enter_new_tasks)
        new_task_button.grid(row=1, column=0, padx=10, pady=10)

        name_label = tk.Label(self.root, text="Task Name:")
        name_label.grid(row=1, column=1, padx=10, pady=10)
        name_entry = tk.Entry(self.root)
        name_entry.grid(row=1, column=2, padx=10, pady=10)
        modify_task_button = tk.Button(self.root, text="Modify Task", command=lambda: self.modify_task(name_entry.get().capitalize()))
        modify_task_button.grid(row=1, column=3, padx=10, pady=10)

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

        # Load stats from JSON file
        try:
            with open('stats.json', 'r') as file:
                stats_data = json.load(file)
        except FileNotFoundError:
            stats_data = []

        # Create a label for the checkbox table
        table_label = tk.Label(self.root, text="Tick all that apply:")
        table_label.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

        # Create checkboxes for each stat name
        check_vars = []
        if stats_data != []:
            for i, attribute in enumerate(stats_data["attributes"]):
                var = tk.BooleanVar()
                check_vars.append([attribute,var])
                checkbox = tk.Checkbutton(self.root, text=attribute, variable=var)
                checkbox.grid(row=4+i, column=0, padx=10, pady=2, columnspan=2)


        def save_new_task():
            name = name_entry.get()
            x = []
            if name:
                for i in check_vars:
                    if i[1].get():
                        x.append(i[0])
                new_task = Task(name, 0, False, datetime.now().strftime('%Y-%m-%d'),x)
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
        tasks_data = [{'name': task.name, 'streak': task.streak, 'updated': task.updated, 'last_updated': task.last_updated, 'attributes': task.attributes} for task in self.page.tasks]
        with open('pstatus.json', 'w') as file:
            json.dump(tasks_data, file, indent=4)

        # Create a backup of the tasks data
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'jsonBackUp')
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, 'pstatus_backup.json')
        with open(backup_file, 'w') as file:
            json.dump(tasks_data, file, indent=4)

    # Clear all widgets from the root window
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    screen = Screen()
    screen.run()