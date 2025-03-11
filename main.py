import tkinter as tk
import json
from datetime import datetime

class Task:
    def __init__(self, name, streak, updated, last_updated):
        self.name = name
        self.updated = updated
        self.streak = streak
        self.last_updated = last_updated

    def __str__(self):
        return f"Task(name={self.name}, updated={self.updated}, streak={self.streak}, last_updated={self.last_updated})"



class Page:
    def __init__(self, tasks):
        self.tasks = tasks

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

    def update_task_status(self, task, var):
        task.updated = var.get()

class Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Status Screen")
        self.root.geometry("1024x768")

        with open('pstatus.json', 'r') as file:
            data = json.load(file)
            self.tasks = [Task(task['name'], task['streak'], task['updated'], task['last_updated']) for task in data]

        self.page = Page(self.tasks)
        self.menu = Menu(self.root, self.page)

    def run(self):
        self.root.mainloop()

class Menu:
    def __init__(self, root, page):
        self.root = root
        self.page = page

        self.label = tk.Label(self.root, text="Task Status Screen")
        self.label.grid(row=0, column=0, padx=10, pady=5, columnspan=2)

        self.button = tk.Button(self.root, text="Tasks", command=self.display_tasks)
        self.button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_tasks)
        self.save_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def streak_check(self,task):
        if task.last_updated != datetime.now().strftime('%Y-%m-%d') and task.updated:
            task.streak += 1
            task.updated = False
        elif task.last_updated != datetime.now().strftime('%Y-%m-%d') and not task.updated:
            task.streak = 0
        task.last_updated = datetime.now().strftime('%Y-%m-%d')
        

    def display_tasks(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        for task in self.page.tasks:
            self.streak_check(task)

        self.save_tasks()

        return_button = tk.Button(self.root, text="Return", command=self.return_to_main)
        return_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        
        new_task_button = tk.Button(self.root, text="Enter New Tasks", command=self.enter_new_tasks)
        new_task_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        
        self.page.display(self.root)

    def enter_new_tasks(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        return_button = tk.Button(self.root, text="Return", command=self.return_to_main)
        return_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        name_label = tk.Label(self.root, text="Task Name:")
        name_label.grid(row=1, column=0, padx=10, pady=5)
        name_entry = tk.Entry(self.root)
        name_entry.grid(row=1, column=1, padx=10, pady=5)

        def save_new_task():
            name = name_entry.get()
            streak = 0
            status = False
            last_updated = datetime.now().strftime('%Y-%m-%d')
            if name:
                new_task = Task(name, streak, status, last_updated)
                self.page.tasks.append(new_task)
                self.save_tasks()
                self.display_tasks()

        enter_button = tk.Button(self.root, text="Enter", command=save_new_task)
        enter_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        name_label.grid(row=2, column=0, padx=10, pady=5)
        name_entry.grid(row=2, column=1, padx=10, pady=5)
        enter_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

    def return_to_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root, self.page)

    def save_tasks(self):
        tasks_data = [{'name': task.name, 'streak': task.streak, 'updated': task.updated, 'last_updated': task.last_updated} for task in self.page.tasks]
        with open('pstatus.json', 'w') as file:
            json.dump(tasks_data, file, indent=4)

    
        

def create_screen():
    screen = Screen()
    screen.run()

def main():
    create_screen()

if __name__ == "__main__":
    main()
