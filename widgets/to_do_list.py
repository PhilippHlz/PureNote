from tkinter import *
from tkinter.font import Font

class ToDoList(Frame):
    def __init__(self, parent, text_style_dto, add_task_button_callback):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        bold_font = Font(weight='bold', size=9)
        regular_font = Font(size=9)

        Label(self, text='ToDo Hinzufügen', font=bold_font).pack(anchor='w')

        Label(self, text='Titel', font=regular_font).pack(anchor='w')
        Entry(self, width=25, font=regular_font).pack(anchor='w')

        Label(self, text='Beschreibung', font=regular_font).pack(anchor='w')
        Text(self, width=25, height=5, font=regular_font).pack(anchor='w')

        Label(self, text='Deine ToDos', font=bold_font, ).pack(anchor='w', pady=(25, 0))