from tkinter import *
from model.paragraph_formats import ParagraphFormats
from dto.text_style_dto import TextStyleDto
from widgets.editor_menu import EditorMenu
from widgets.timer import Timer
from widgets.editor import Editor
from widgets.to_do_list import ToDoList
from widgets.html_exporter import HtmlExporter

class App(Tk):
    """
    Die Hauptanwendungsklasse, die das Hauptfenster und alle Widgets initialisiert.
    Stellt die Verbindung zwischen den verschiedenen Widgets und Datenmodellen her.
    """
    def __init__(self):
        super().__init__()
        self.title('The Pure Note Project')
        self.geometry('1280x720')

        # Grid-Layout mit 3 Spalten
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # Rechter Frame
        self.right_panel = Frame(self)
        self.right_panel.grid(row=0, column=2, sticky='n', padx=15, pady=15)

        # Data
        self.paragraph_formats = ParagraphFormats()
        self.text_style_dto = TextStyleDto(self, 'p', self.paragraph_formats.get_style_preset('p'))

        # Widgets
        self.to_do_list = ToDoList(self, self.on_add_task_button_click, self.on_checkbutton_clicked)
        self.editor = Editor(self, self.paragraph_formats, self.text_style_dto)
        self.editor_menu = EditorMenu(self.right_panel, self.paragraph_formats, self.text_style_dto, self.on_update_button_click)
        self.timer = Timer(self.right_panel, 30, 30)
        self.exporter = HtmlExporter(self.right_panel, self.editor)

        # Traces um auf Änderungen aus dem Menü zu reagieren (Absatzformat & Inline-Stil)
        self.text_style_dto.set_paragraph_format_trace(self.on_paragraph_format_change)
        self.text_style_dto.set_inline_trace(self.on_inline_style_change)

        # Start
        self.mainloop()

    def on_add_task_button_click(self):
        """
        Wird getriggert, wenn der Add-Button im ToDoList-Widget geklickt wird.
        Es wird die neu erstellte Task zurückgegeben und im Editor der ausgewählte Text farblich passend hervorgehoben.
        Wenn keine Auswahl im Editor vorhanden ist, wird nur die Task erstellt aber nichts hervorgehoben.
        """

        # Erstelle eine neue Task und markiere die Auswahl im Editor verwendend den Titel als tag und die Farbe der Task
        task = self.to_do_list.add_task()
        self.editor.highlight_selection(task.title, task.color)

    def on_checkbutton_clicked(self, title):
        """
        Wird getriggert, wenn ein Checkbutton im ToDoList-Widget geklickt wird.
        Wenn der Checkbutton aktiviert wird, wird der entsprechende Tag im Editor entfernt.
        """
        self.editor.remove_tag(title)

    def on_paragraph_format_change(self, *_):
        """
        Wird jedes mal getriggert, wenn sich das Absatzformat ändert.
        Um einen erneuten Trace zu verhindern, wird zuerst geprüft, ob trace_break gesetzt ist,
        sonst würde für jedes Sets des TextStyleDTO noch ein Trace getriggert werden.
        Zuerst wird anhand des keys des DTOS ein Preset aus den ParagraphFormats geholt,
        dann wird das TextStyleDTO mit dem neuen Preset aktualisiert.
        Danach wird der aktuelle Token im Editor gesetzt und der Stil auf die gesamte Zeile angewendet.
        """

        # Wenn bereits ein Trace getriggert wurde, abbrechen um mehrfache Traces zu verhindern
        if self.text_style_dto.trace_break:
            return

        # Hole den aktuellen paragraph_key und das zugehörige Preset
        paragraph_key = self.text_style_dto.paragraph_key.get()
        preset = self.paragraph_formats.get_style_preset(paragraph_key)

        # Setze das DTO mit dem Preset und setze den Stil im Editor auf den ganzen Absatz
        self.text_style_dto.set_text_style_dto(paragraph_key, preset)
        self.editor.set_current_token()
        self.editor.apply_style_to_line()

    def on_inline_style_change(self, *_):
        """
        Wird jedes mal getriggert, wenn sich der Inline-Stil ändert.
        Um einen erneuten Trace zu verhindern, wird zuerst geprüft, ob trace_break gesetzt ist,
        sonst würde für jedes Sets des TextStyleDTO noch ein Trace getriggert werden.
        Danach wird der aktuelle Token im Editor gesetzt und der Stil auf die Auswahl angewendet.
        """

        # Wenn bereits ein Trace getriggert wurde, abbrechen um mehrfache Traces zu verhindern
        if self.text_style_dto.trace_break:
            return

        # Setze den aktuellen Token im Editor und wende den Stil auf die Auswahl an.
        # Wenn keine Auswahl vorhanden ist, wird nur der Token gesetzt, um in diesem Stil weiterzuschreiben.
        self.editor.set_current_token()
        self.editor.apply_style_to_selection()

    def on_update_button_click(self, *_):
        """
        Wird getriggert, wenn der Update-Button im EditorMenu geklickt wird.
        Aktualisiert den Preset-Stil im Editor und wendet den neuen Stil auf alle Absätze an die das gleiche Absatzformat haben.
        """
        self.editor.update_preset_style()

    def on_export(self):
        """
        Wird getriggert, wenn der HTML exportieren Button im EditorMenu geklickt wird.
        Öffnet einen Speichern-Dialog und exportiert den Inhalt des Editors als HTML-Datei.
        """
        self.exporter.export()

if __name__ == '__main__':
    app = App()