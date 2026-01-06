from tkinter import *
from tkinter.font import Font
import random

class ToDoList(Frame):
    def __init__(self, parent, on_add_task_button_callback, on_delete_task_callback):
        """
        Erstellt das ToDoList-Widget, welches genutzt wird um ToDos hinzuzufügen und zu entfernen.
        Es ermöglicht es ToDos mit Entry-Widgets Titel und Beschreibung hinzuzufügen.
        Mit diesen Werten wird ein Task-Widget erstellt und der to_do_list hinzugefügt.
        Die Task-Widgets werden in der to_do_list gespeichert, damit die 'id' hier der titel unique ist
        und der Editor diesen als Tag verwenden kann.
        """
        super().__init__(master=parent)
        self. on_delete_task_callback = on_delete_task_callback
        self.to_do_list = {}

        self.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)

        self.bold_font = Font(weight='bold', size=9)
        self.regular_font = Font(size=9)

        Label(self, text='ToDo Hinzufügen', font=self.bold_font).pack(anchor='w')

        # Titel
        Label(self, text='Titel', font=self.regular_font).pack(anchor='w')
        self.title = Entry(self, width=25, font=self.regular_font)
        self.title.pack(anchor='w')

        # Beschreibung
        Label(self, text='Beschreibung', font=self.regular_font).pack(anchor='w')
        self.description = Entry(self, width=25, font=self.regular_font)
        self.description.pack(anchor='w')

        # Task hinzufügen Button
        Button(self, text='ToDo hinzufügen', command=on_add_task_button_callback).pack(anchor='w')

        Label(self, text='Deine ToDos', font=self.bold_font).pack(anchor='w', pady=(25, 10))
        

    def add_task(self):
        """
        Wird getriggert, wenn der Add-Button in app geklickt wird durch callback.
        Wenn der Titel nicht leer ist und noch nicht vorhanden ist,
        wird ein neuer Task erstellt und der to_do_list hinzugefügt.
        Danach werden die Textfelder geleert.
        :return: Task die erstellt wurde
        """
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
        """
        Erstellt eine callback Funktion für den Checkbutton, sodass dieser die Task aus der to_do_list entfernt.
        Wenn der Checkbutton geklickt wird, wird diese Funktion aufgerufen und der Titel der Task übergeben.
        """
        if title in self.to_do_list:
            del self.to_do_list[title] # Entfernt Task aus der to_do_list
        self.on_delete_task_callback(title) # Entfernt Task aus dem Editor

class Task(Frame):
    """
    Erstellt ein Task-Widget, welches eine Repräsentation eines Eintrags in der to_do_list ist.
    Sie besteht aus einem farbigen linken Balken, einem Titel und einer Beschreibung und einem Checkbutton zum Abhaken.
    """
    def __init__(self, parent, title, description, delete_callback):
        super().__init__(master=parent)
        self.title = title
        self.description = description
        self.color = self._generate_random_color()
        self.delete_callback = delete_callback

        # Hauptcontainer
        container = Frame(self)
        container.pack(fill='x', pady=(0, 5))

        # Farbige linker Balken
        left_border = Frame(container, bg=self.color, width=5)
        left_border.pack(side='left', fill='y')

        # Obere Inhaltscontainer
        top_content = Frame(container)
        top_content.pack(fill='x')
        Label(top_content, text=self.title, wraplength=200, justify='left', anchor='w').pack(side='left', fill='x')
        Checkbutton(top_content, command=self._delete_self).pack(side='right')

        # Untere Inhaltscontainer, wenn Beschreibung vorhanden ist
        if self.description.strip():
            bottom_content = Frame(container)
            bottom_content.pack(fill='x')
            Label(bottom_content, text=self.description, wraplength=200, justify='left', anchor='w').pack(fill='x')

        self.pack(fill='x')

    def _delete_self(self):
        """
        Wird getriggert, wenn der Checkbutton in Task geklickt wird.
        Hier wird die methode aus ToDoList aufgerufen und der Titel der Task übergeben.
        Damit wird der Task aus der to_do_list entfernt und aus dem Editor entfernt.
        """
        self.delete_callback(self.title) # Entfernt Task aus der to_do_list und aus dem Editor
        self.destroy() # Zerstört das Task-Widget

    @staticmethod
    def _generate_random_color():
        """
        Generiert eine zufällige Farbe in Hexadezimal.
        """
        letters = "0123456789ABCDEF"
        color = "#"
        for i in range(6):
            color += random.choice(letters)
        return color
