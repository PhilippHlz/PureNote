from tkinter import StringVar


class ToDoDto:
    def __init__(self, parent):
        self.title = StringVar(master=parent)
        self.description = StringVar(master=parent)
        self.color = StringVar(master=parent)