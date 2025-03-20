import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import math
from datetime import datetime
import os

class StatusScreen:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Anime Status Screen")
        self.root.geometry("800x600")
        
        # Initialize data files
        self.stats_file = "stats.json"
        self.tasks_file = "pstatus.json"
        self.stats_data = self.load_stats()
        self.task_data = self.load_tasks()
        
        # Configure main UI
        self.setup_ui()
        self.root.mainloop()
    
    def load_stats(self):
        # Load stats data from file
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"attributes": {}}
    
    def load_tasks(self):
        # Load tasks data from file
        try:
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"tasks": {}}
    
    def save_stats(self):
        # Save stats data to file and create a backup
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats_data, f, indent=2)
        
        backup_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'jsonBackUp'))
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.abspath(os.path.join(backup_dir, 'stats.json'))
        with open(backup_file, 'w') as file:
            json.dump(self.stats_data, file, indent=2)
    
    def save_tasks(self):
        # Save tasks data to file and create a backup
        with open(self.tasks_file, 'w') as f:
            json.dump(self.task_data, f, indent=2)

    def setup_ui(self):
        # Setup the main UI components
        control_frame = tk.Frame(self.root, bg="#2c2c2c")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(control_frame, text="Add Attribute", command=self.add_attribute, 
                 bg="#4a4a4a", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Delete Attribute", command=self.delete_attribute,
                 bg="#4a4a4a", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Calculate Status", command=self.calculate_status,
                 bg="#4a4a4a", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Visualization Canvas
        self.canvas = tk.Canvas(self.root, width=600, height=500, bg="black")
        self.canvas.pack(pady=10)
        
        self.create_status_board()
        self.update_status_board()
    
    def add_attribute(self):
        # Add a new attribute to the stats
        attribute = simpledialog.askstring("New Attribute", "Enter attribute name:").capitalize()
        if attribute:
            if attribute not in self.stats_data["attributes"]:
                self.stats_data["attributes"][attribute] = 0
                self.save_stats()
                self.create_status_board()
                self.update_status_board()
            else:
                messagebox.showwarning("Exists", "Attribute already exists!")
    
    def delete_attribute(self):
        # Delete an existing attribute from the stats
        attribute = simpledialog.askstring("Remove Attribute", "Enter attribute name:")
        if attribute and attribute in self.stats_data["attributes"]:
            del self.stats_data["attributes"][attribute]
            self.save_stats()
            self.create_status_board()
            self.update_status_board()
        else:
            messagebox.showwarning("Error", "Attribute not found!")
    
    def calculate_status(self):
        # Calculate the status based on task data
        for attr in self.stats_data["attributes"]:
            self.stats_data["attributes"][attr] = 0

        # Update stats based on task data
        for task in self.task_data:
            for attr in task["attributes"]:
                self.stats_data["attributes"][attr] += task["streak"]

        self.save_stats()
        self.save_tasks()
        self.update_status_board()
    
    def create_status_board(self):
        # Create the status board visualization
        self.canvas.delete("grid")
        attributes = list(self.stats_data["attributes"].keys())
        num_attr = len(attributes)
        center_x, center_y = 300, 250
        max_radius = 200
        
        # Create concentric polygons
        for level in range(1, 11):
            radius = max_radius * (level/10)
            points = []
            for i in range(num_attr if num_attr > 2 else 3):
                angle = 2 * math.pi * i / (num_attr if num_attr > 2 else 3)
                x = center_x + radius * math.cos(angle - math.pi/2)
                y = center_y + radius * math.sin(angle - math.pi/2)
                points.extend([x, y])
            
            self.canvas.create_polygon(
                points,
                outline="#373737",
                fill="",
                tags="grid",
                width=1
            )

            values = list(self.stats_data["attributes"].values())
            max_value = max(values) if max(values) > 10 else 10

            # Create a label using canvas
            self.canvas.create_text(
                points[0]+5, points[1]+10,
                text=str(math.ceil(max_value/11)*level),
                fill="white",
                font=("Arial", 8),
                tags="grid"
            )
        
        # Create attribute labels
        if num_attr > 0:
            label_radius = max_radius + 30
            for i, attr in enumerate(attributes):
                angle = 2 * math.pi * i / num_attr - math.pi/2
                x = center_x + label_radius * math.cos(angle)
                y = center_y + label_radius * math.sin(angle)
                self.canvas.create_text(
                    x, y,
                    text=attr.upper(),
                    fill="white",
                    font=("Arial", 10, "bold"),
                    tags="grid"
                )
    
    def update_status_board(self):
        # Update the status board visualization
        self.canvas.delete("status")
        attributes = list(self.stats_data["attributes"].keys())
        values = list(self.stats_data["attributes"].values())
        num_attr = len(attributes)
        
        if num_attr < 1:
            return
        
        max_value = max(values) if max(values) > 0 else 1
        normalized = [v/max_value for v in values]
        
        center_x, center_y = 300, 250
        max_radius = 200
        points = []
        
        for i, value in enumerate(normalized):
            angle = 2 * math.pi * i / num_attr - math.pi/2
            radius = max_radius * value
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.extend([x, y])
        
        # Draw status polygon
        self.canvas.create_polygon(
            points,
            outline="#00ffff",
            fill="#00ff22",
            stipple="gray50",
            width=2,
            tags="status"
        )

if __name__ == "__main__":
    StatusScreen()