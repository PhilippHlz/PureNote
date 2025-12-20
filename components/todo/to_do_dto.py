from tkinter import *
import random

class TaskDto:
    def __init__(self, title, description, color):
        self.title = StringVar(value=title)
        self.description = StringVar(value=description)
        self.color = StringVar(value=color)
