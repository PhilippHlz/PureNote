from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox

from model.paragraph_formats import ParagraphFormats
from dto.text_style_dto import TextStyleDto

from widgets.editor_menu import EditorMenu
from widgets.editor import Editor
from widgets.to_do_list import ToDoList
from widgets.timer import Timer

from components.export.html_exporter import export_editor_to_html


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('The Pure Note Project')
        self.geometry('1280x720')

        # Grid-Layout mit 3 Spalten
        # Spalte 0: linker Panel (ToDo + Timer)
        # Spalte 1: Editor (groß)
        # Spalte 2: EditorMenu (rechts)
        LEFT_PANEL_WIDTH = 270  # <- hier kannst du easy feintunen (z.B. 300 / 340)

        self.grid_columnconfigure(0, weight=0, minsize=LEFT_PANEL_WIDTH)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Nur eine "Hauptzeile" im Root-Grid
        self.grid_rowconfigure(0, weight=1)

        # Data
        self.paragraph_formats = ParagraphFormats()
        self.text_style_dto = TextStyleDto(self, 'p', self.paragraph_formats.get_style_preset('p'))

        # ===== Left Panel =====
        self.left_panel = Frame(self, width=LEFT_PANEL_WIDTH)
        # links schöner Rand, aber nach rechts KEIN extra Abstand zum Editor
        self.left_panel.grid(row=0, column=0, sticky='ns', padx=(15, 0), pady=15)

        # Wichtig: verhindert, dass Canvas/Timer den linken Panel breiter zieht
        self.left_panel.grid_propagate(False)

        # Left panel hat 2 Zeilen: oben ToDos (dehnbar), unten Timer (fix)
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(1, weight=0)

        # Widgets
        self.to_do_list = ToDoList(self.left_panel, self.on_add_task_button_click, self.on_checkbutton_clicked)
        self.to_do_list.grid(row=0, column=0, sticky='nsew')

        # Timer
        self.timer = Timer(self.left_panel, 30, 5)
        self.timer.grid(row=1, column=0, sticky='ew', pady=(10, 0))

        # ===== Mitte / Rechts =====
        self.editor = Editor(self, self.paragraph_formats, self.text_style_dto)
        # FIX: links 0 Abstand -> Textfeld rutscht sichtbar nach links
        self.editor.grid(row=0, column=1, sticky='nsew', padx=(0, 15), pady=15)

        # EditorMenu bekommt zusätzlich den Export-Callback
        self.editor_menu = EditorMenu(
            self,
            self.paragraph_formats,
            self.text_style_dto,
            self.on_update_button_click,
            self.on_export_html_click
        )
        self.editor_menu.grid(row=0, column=2, sticky='ns', padx=(0, 15), pady=15)

        # Traces
        self.text_style_dto.set_paragraph_format_trace(self.on_paragraph_format_change)
        self.text_style_dto.set_inline_trace(self.on_inline_style_change)

        self.mainloop()

    def on_paragraph_format_change(self, *_):
        """
        Wird jedes mal getriggert, wenn sich das Absatzformat ändert.
        Um einen erneuten Trace zu verhindern, wird zuerst geprüft, ob trace_break gesetzt ist,
        sonst würde für jedes Sets des TextStyleDTO noch ein Trace getriggert werden.
        Zuerst wird anhand des keys des DTOS ein Preset aus den ParagraphFormats geholt,
        dann wird das TextStyleDTO mit dem neuen Preset aktualisiert.
        Danach wird der aktuelle Token im Editor gesetzt und der Stil auf die gesamte Zeile angewendet.
        """
        if self.text_style_dto.trace_break:
            return
        key = self.text_style_dto.paragraph_key.get()
        preset = self.paragraph_formats.get_style_preset(key)
        self.text_style_dto.set_text_style_dto(key, preset)

        self.editor.set_current_token()
        self.editor.apply_style_to_line()

    def on_inline_style_change(self, *_):
        """
        Wird jedes mal getriggert, wenn sich der Inline-Stil ändert.
        Um einen erneuten Trace zu verhindern, wird zuerst geprüft, ob trace_break gesetzt ist,
        sonst würde für jedes Sets des TextStyleDTO noch ein Trace getriggert werden.
        Danach wird der aktuelle Token im Editor gesetzt und der Stil auf die Auswahl angewendet.
        """
        if self.text_style_dto.trace_break:
            return

        self.editor.set_current_token()
        self.editor.apply_style_to_selection()

    def on_update_button_click(self, *_):
        """
        Wird getriggert, wenn der Update-Button im EditorMenu geklickt wird.
        Aktualisiert den Preset-Stil im Editor und wendet den neuen Stil auf alle Absätze an die das gleiche Absatzformat haben.
        """
        self.editor.update_preset_style()

    def on_export_html_click(self):
        """
        Wird getriggert, wenn der HTML exportieren Button im EditorMenu geklickt wird.
        Öffnet einen Speichern-Dialog und exportiert den Inhalt des Editors als HTML-Datei.
        """
        filename = asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML-Dateien", "*.html"), ("Alle Dateien", "*.*")],
            initialfile="export.html",
            title="HTML Export speichern"
        )
        if not filename:
            return

        try:
            export_editor_to_html(self.editor, filename)
            messagebox.showinfo("Export", "HTML Export erfolgreich gespeichert.")
        except Exception as e:
            messagebox.showerror("Export fehlgeschlagen", f"Beim Export ist ein Fehler aufgetreten:\n{e}")

    def on_add_task_button_click(self):
        """
        Wird getriggert, wenn der Add-Button im ToDoList-Widget geklickt wird.
        Es wird ein neuer Task im ToDoList-Widget hinzugefügt und wenn eine Auswahl im Editor vorhanden ist,
        wird der Text der Auswahl farblich passend hervorgehoben.
        Dabei wird im Editor ein neues Tag erstellt, das mit dem Titel des Tasks übereinstimmt.
        """
        task = self.to_do_list.add_task()
        if task:
            self.editor.highlight_selection(task.title, task.color)

    def on_checkbutton_clicked(self, title):
        """
        Wird getriggert, wenn ein Checkbutton im ToDoList-Widget geklickt wird.
        Es werden alle Tags entfernt, die mit dem Titel des Checkbuttons übereinstimmen.
        """
        self.editor.remove_tag(title)


if __name__ == '__main__':
    app = App()
