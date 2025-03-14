import tkinter as tk
from tkinter import messagebox
import math
import random

def on_button_click():
    messagebox.showinfo("Information", "Button clicked!")

class RandomiserApp:
    def __init__(self,tasks):
        self.root = tk.Tk()
        self.root.title("Randomiser")
        
        self.canvas = tk.Canvas(self.root, width=1024, height=1024)
        self.canvas.pack(pady=10)
        
        self.center_x = self.canvas.winfo_reqwidth() / 2
        self.center_y = self.canvas.winfo_reqheight() / 2
        self.radius = 400

        self.tasks = tasks
        
        self.draw_wheel()
        self.draw_spokes()
        self.add_spin_button()
    
    def draw_wheel(self):
        self.canvas.create_oval(self.center_x - self.radius, self.center_y - self.radius, 
                                self.center_x + self.radius, self.center_y + self.radius, 
                                outline="black", fill="white")
    
    def draw_spokes(self,increment=0):
        for i in range(len(self.tasks)):
            cangle = i * (360 / len(self.tasks)) + increment
            mangle = i* (360 / len(self.tasks)) + increment + (360 / len(self.tasks) / 2)
            x = self.center_x + self.radius * math.cos(math.radians(cangle))
            y = self.center_y + self.radius * math.sin(math.radians(cangle))
            
            self.canvas.create_line(self.center_x, self.center_y, x, y, fill="black")

            x = self.center_x + self.radius * math.cos(math.radians(mangle))*0.7
            y = self.center_y + self.radius * math.sin(math.radians(mangle))*0.7
            display_text = self.tasks[i].name if len(self.tasks[i].name) <= 10 else self.tasks[i].name[:10] + "..."
            self.canvas.create_text(x, y, text=display_text, font=("Helvetica", 16))

    def spin_wheel(self):
        self.target_angle = random.randint(20,30)*20
        self.angle = 0
        self.animate_spin()
        selected_task_index = 0
        for i in range(len(self.tasks)):
            if ((i)* (360 / len(self.tasks)) + self.target_angle - 90 )%360 < 180 < ((i+1)* (360 / len(self.tasks)) + self.target_angle - 90 )%360:
                selected_task_index = i
                break
        selected_task = self.tasks[selected_task_index]
        self.root.after(1000, lambda: messagebox.showinfo("Selected Task", f"The selected task is: {selected_task.name}"))

    def animate_spin(self):
        if self.angle < self.target_angle:
            self.canvas.delete("all")
            self.draw_wheel()
            self.draw_spokes(self.angle)
            self.angle += 1
            self.root.after(1, self.animate_spin)

    def add_spin_button(self):
        self.spin_button = tk.Button(self.root, text="Spin Wheel", command=self.spin_wheel)
        self.spin_button.pack(pady=10)
        self.spin_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomiserApp(root,["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"])
    root.mainloop()