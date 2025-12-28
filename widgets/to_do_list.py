from tkinter import *
from tkinter.font import Font
import random

class ToDoList(Frame):
    def __init__(self, parent, on_add_task_button_callback, on_delete_task_callback):
        super().__init__(master=parent)
        self. on_delete_task_callback = on_delete_task_callback
        self.to_do_list = {}

        self.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        self.bold_font = Font(weight='bold', size=9)
        self.regular_font = Font(size=9)

        Label(self, text='ToDo Hinzufügen', font=self.bold_font).pack(anchor='w')

        Label(self, text='Titel', font=self.regular_font).pack(anchor='w')
        self.title = Entry(self, width=25, font=self.regular_font)
        self.title.pack(anchor='w')

        Label(self, text='Beschreibung', font=self.regular_font).pack(anchor='w')
        self.description = Entry(self, width=25, font=self.regular_font)
        self.description.pack(anchor='w')

        Button(self, text='ToDo hinzufügen', command=on_add_task_button_callback).pack(anchor='w')

        Label(self, text='Deine ToDos', font=self.bold_font).pack(anchor='w', pady=(25, 10))

    def add_task(self):
        title = self.title.get().strip()
        description = self.description.get().strip()

        if not title or title in self.to_do_list:
            return None

        task = Task(self, title, description, delete_callback=self.remove_task)
        self.to_do_list[title] = task

        self.title.delete(0, END)
        self.description.delete(0, END)
        return task

    def remove_task(self, title):
        if title in self.to_do_list:
            del self.to_do_list[title]
        self.on_delete_task_callback(title)

class Task(Frame):
    def __init__(self, parent, title, description, delete_callback):
        super().__init__(master=parent)
        self.title = title
        self.description = description
        self.color = self._generate_random_color()
        self.delete_callback = delete_callback

        container = Frame(self)
        container.pack(fill='x', pady=(0, 5))

        left_border = Frame(container, bg=self.color, width=5)
        left_border.pack(side='left', fill='y')

        top_content = Frame(container)
        top_content.pack(fill='x')
        Label(top_content, text=self.title, wraplength=200, justify='left', anchor='w').pack(side='left', fill='x')
        Checkbutton(top_content, command=self._delete_self).pack(side='right')

        if self.description.strip():
            bottom_content = Frame(container)
            bottom_content.pack(fill='x')
            Label(bottom_content, text=self.description, wraplength=200, justify='left', anchor='w').pack(fill='x')

        self.pack(fill='x')

    def _delete_self(self):
        self.delete_callback(self.title)
        self.destroy()

    @staticmethod
    def _generate_random_color():
        letters = "0123456789ABCDEF"
        color = "#"
        for i in range(6):
            color += random.choice(letters)
        return color