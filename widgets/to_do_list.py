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

        # NOTE: Kein eigenes .grid() hier mehr in den Parent rein!
        # Das macht App.py zentral, damit das Layout stabil bleibt.
        self.configure(padx=15, pady=15)

        self.bold_font = Font(weight='bold', size=9)
        self.regular_font = Font(size=9)

        # Layout intern (Input oben, Tasks scrollen unten)
        self.grid_rowconfigure(0, weight=0)  # input area
        self.grid_rowconfigure(1, weight=0)  # header "Deine ToDos"
        self.grid_rowconfigure(2, weight=1)  # scroll area
        self.grid_columnconfigure(0, weight=1)

        # --- UI: Input Bereich (fix) ---
        top = Frame(self)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_columnconfigure(0, weight=1)

        Label(top, text='ToDo Hinzufügen', font=self.bold_font).pack(anchor='w')

        # Titel
        Label(top, text='Titel', font=self.regular_font).pack(anchor='w')
        self.title = Entry(top, width=25, font=self.regular_font)
        self.title.pack(anchor='w')

        # Beschreibung
        Label(top, text='Beschreibung', font=self.regular_font).pack(anchor='w')
        self.description = Entry(top, width=25, font=self.regular_font)
        self.description.pack(anchor='w')

        # Task hinzufügen Button
        Button(top, text='ToDo hinzufügen', command=on_add_task_button_callback).pack(anchor='w')

        header = Frame(self)
        header.grid(row=1, column=0, sticky="ew")
        Label(header, text='Deine ToDos', font=self.bold_font).pack(anchor='w', pady=(25, 10))
        #ToDo: tasks scrollbar machen geht wohl mit canvas und scrollbar

        # --- Scrollbarer Bereich nur für Tasks ---
        self.tasks_wrapper = Frame(self)
        self.tasks_wrapper.grid(row=2, column=0, sticky="nsew")

        self.tasks_canvas = Canvas(self.tasks_wrapper, highlightthickness=0, bd=0)
        self.tasks_scrollbar = Scrollbar(self.tasks_wrapper, orient='vertical', command=self.tasks_canvas.yview)
        self.tasks_canvas.configure(yscrollcommand=self.tasks_scrollbar.set)

        self.tasks_canvas.pack(side='left', fill='both', expand=True)
        # Scrollbar wird nur angezeigt, wenn wirklich nötig
        # (damit die linke Spalte nicht “wackelt” / unnötig breiter wirkt)

        self.tasks_frame = Frame(self.tasks_canvas)
        self._tasks_window_id = self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor='nw')

        # Events zum updaten
        self.tasks_frame.bind("<Configure>", self._on_tasks_frame_configure)
        self.tasks_canvas.bind("<Configure>", self._on_canvas_configure)

        # Mousewheel nur, wenn Maus über dem Canvas ist (kein globales bind_all)
        self.tasks_canvas.bind("<Enter>", self._bind_mousewheel)
        self.tasks_canvas.bind("<Leave>", self._unbind_mousewheel)

        # initial
        self._update_scrollbar_visibility()

    def _bind_mousewheel(self, _event=None):
        self.tasks_canvas.bind_all("<MouseWheel>", self._on_mousewheel)      # Windows / Mac
        self.tasks_canvas.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux up
        self.tasks_canvas.bind_all("<Button-5>", self._on_mousewheel_linux)  # Linux down

    def _unbind_mousewheel(self, _event=None):
        self.tasks_canvas.unbind_all("<MouseWheel>")
        self.tasks_canvas.unbind_all("<Button-4>")
        self.tasks_canvas.unbind_all("<Button-5>")

    def _on_tasks_frame_configure(self, _event):
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        self._update_scrollbar_visibility()

    def _on_canvas_configure(self, event):
        # Canvas-Breite an Task-Frame weiterreichen, damit Tasks nicht abgeschnitten werden
        self.tasks_canvas.itemconfig(self._tasks_window_id, width=event.width)
        self._update_scrollbar_visibility()

    def _scrollbar_needed(self):
        self.update_idletasks()
        content_height = self.tasks_frame.winfo_reqheight()
        visible_height = self.tasks_canvas.winfo_height()
        return content_height > visible_height + 2  # +2 als kleiner Puffer

    def _update_scrollbar_visibility(self):
        if self._scrollbar_needed():
            if not self.tasks_scrollbar.winfo_ismapped():
                self.tasks_scrollbar.pack(side='right', fill='y')
        else:
            if self.tasks_scrollbar.winfo_ismapped():
                self.tasks_scrollbar.pack_forget()
            self.tasks_canvas.yview_moveto(0)

    def _on_mousewheel(self, event):
        if self._scrollbar_needed():
            self.tasks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        if self._scrollbar_needed():
            if event.num == 4:
                self.tasks_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.tasks_canvas.yview_scroll(1, "units")

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

        # Task in den scrollbaren tasks_frame packen (nicht direkt in self)
        task = Task(self.tasks_frame, title, description, delete_callback=self.remove_task)
        self.to_do_list[title] = task

        self.title.delete(0, END)
        self.description.delete(0, END)

        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        self._update_scrollbar_visibility()
        return task

    def remove_task(self, title):
        """
        Erstellt eine callback Funktion für den Checkbutton, sodass dieser die Task aus der to_do_list entfernt.
        Wenn der Checkbutton geklickt wird, wird diese Funktion aufgerufen und der Titel der Task übergeben.
        """
        if title in self.to_do_list:
            del self.to_do_list[title] # Entfernt Task aus der to_do_list
        self.on_delete_task_callback(title) # Entfernt Task aus dem Editor

        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        self._update_scrollbar_visibility()

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
