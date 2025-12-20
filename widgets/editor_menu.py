from tkinter import *
from tkinter.font import Font
from tkinter import font

class EditorMenu(Frame):
    """
    Stellt das rechte Menü für die Textformatierung im Editor bereit.
    Ermöglicht die Auswahl von Absatzformaten, Schriftarten, Schriftgrößen und Inline-Stilen.
    Die werte werden über ein TextStyleDTO verwaltet, wenn sich diese ändern, werden die entsprechenden Traces getriggert.
    Bei Klick auf den Update-Button wird eine Callback-Funktion ausgeführt, die im App-Klasse definiert ist.
    """
    def __init__(self, parent, paragraph_formats, text_style_dto, update_button_callback):
        super().__init__(master=parent)
        self.grid(row=0, column=2, sticky='nsew', padx=15, pady=15)
        self._create_grid(4, 10)
        bold_font = Font(weight='bold', size=9)
        regular_font = Font(size=9)

        # Absatzformat
        Label(self, text='Absatzformat', font=bold_font).grid(row=0, columnspan=4, sticky='w')
        paragraph_format_menu = OptionMenu(self, text_style_dto.paragraph_key, *paragraph_formats.style_presets.keys())
        paragraph_format_menu.grid(row=1, column=0, columnspan=4, sticky='ew')

        # Absatzformat aktualisieren Button
        update_paragraph_format_button = Button(self, text='Absatzformat aktualisieren', command=update_button_callback)
        update_paragraph_format_button.grid(row=2, columnspan=4, sticky='ew')

        # Schriftfamilie
        Label(self, text='Schrift', font=bold_font).grid(row=3, columnspan=4, sticky='w', pady=(25, 0))
        font_family_menu = OptionMenu(self, text_style_dto.family, *font.families())
        font_family_menu.grid(row=4, columnspan=3, sticky='ew')

        # Schriftgröße
        font_size_menu = OptionMenu(self, text_style_dto.size, *list(range(8, 42)))
        font_size_menu.grid(row=4, column=3, columnspan=1, sticky='ew')

        # Bold Checkbutton
        bold_checkbutton = Checkbutton(self, text='B', variable=text_style_dto.bold)
        bold_checkbutton.grid(row=5, column=0, columnspan=1, sticky='w')

        # Italic Checkbutton
        italic_checkbutton = Checkbutton(self, text='I', variable=text_style_dto.italic)
        italic_checkbutton.grid(row=5, column=1, columnspan=1, sticky='w')

        # Underline Checkbutton
        underline_checkbutton = Checkbutton(self, text='U', variable=text_style_dto.underline)
        underline_checkbutton.grid(row=5, column=2, columnspan=1, sticky='w')

        # Highlight Checkbutton
        highlight_checkbutton = Checkbutton(self, text='H', variable=text_style_dto.highlight)
        highlight_checkbutton.grid(row=5, column=3, columnspan=1, sticky='w')

        # Farbfeld
        color_entry = Entry(self, textvariable=text_style_dto.color, width=8)
        color_entry.grid(row=6, columnspan=4, sticky='ew')

        # Zeilenabstand
        Label(self, text='Zeilenabstand', font=bold_font).grid(row=7, columnspan=4, sticky='w', pady=(25, 0))
        line_height_spinbox = Spinbox(self, from_=1, to=100, increment=1, textvariable=text_style_dto.line_height, width=3)
        line_height_spinbox.grid(row=8, columnspan=4, sticky='ew')

        # Abstand vor Absatz
        Label(self, text='Abstand vor Absatz', font=regular_font).grid(row=9, columnspan=3, sticky='w')
        space_before_spinbox = Spinbox(self, from_=0, to=100, increment=1, textvariable=text_style_dto.space_before, width=3)
        space_before_spinbox.grid(row=9, column=3, columnspan=1, sticky='ew')

        # Abstand nach Absatz
        Label(self, text='Nach dem Absatz', font=regular_font).grid(row=10, columnspan=3, sticky='w')
        space_after_spinbox = Spinbox(self, from_=0, to=100, increment=1, textvariable=text_style_dto.space_after, width=3)
        space_after_spinbox.grid(row=10, column=3, columnspan=1, sticky='ew')

    def _create_grid(self, column, row):
        """
        Erstellt ein Grid-Layout mit der angegebenen Anzahl an Spalten und Zeilen.
        
        :param column: Spaltenanzahl
        :param row: Zeilenanzahl
        """
        for i in range(column):
            self.grid_columnconfigure(i)
        for i in range(row):
            self.grid_rowconfigure(i)