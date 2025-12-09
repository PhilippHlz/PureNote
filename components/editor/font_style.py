import tkinter.font as tk_font

class FontStyle:
    def __init__(self, name, family, size, weight, color):
        self.name = name
        self.family = family
        self.size = size
        self.weight = weight
        self.color = color
        self.font = None

    def create_font(self):
        self.font = tk_font.Font(family=self.family, size=self.size, weight=self.weight)