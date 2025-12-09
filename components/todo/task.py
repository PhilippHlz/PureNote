import tkinter as tk
import random

class Task(tk.Frame):
    def __init__(self, master, title, description, boolean_var):
        super().__init__(master)
        self.title = title
        self.description = description
        self.check_status = boolean_var
        self.color = self._generate_random_color()

    #todo: Style hinzufügen
    def render(self):

        top_frame = tk.Frame(self, bg=self.color)
        top_frame.pack(fill="x")

        title_label = tk.Label(top_frame, text=self.title, bg=self.color)
        title_label.pack(side="left")

        checkbutton = tk.Checkbutton(top_frame, variable=self.check_status, bg=self.color)
        checkbutton.pack(side="right")

        if not self.description == "":
            bottom_frame = tk.Frame(self, bg=self.color)
            bottom_frame.pack(fill="x", side="left", pady=(0, 10))

            description_label = tk.Label(bottom_frame, text=self.description)
            description_label.pack(fill="x")

        self.pack(fill="x")

    @staticmethod
    def _generate_random_color():
        letters = "0123456789ABCDEF"
        color = "#"
        for i in range(6):
            color += random.choice(letters)
        return color