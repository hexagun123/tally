import tkinter as tk
import json
from datetime import datetime
import classes

Task = classes.Task
Page = classes.Page
Screen = classes.Screen
Menu = classes.Menu


# Create and run the screen
def create_screen():
    screen = Screen()
    screen.run()

def main():
    create_screen()

if __name__ == "__main__":
    main()
