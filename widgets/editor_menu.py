from tkinter import *
from tkinter.font import Font
from tkinter import font


class EditorMenu(Frame):
    """
    Stellt das rechte Menü für die Textformatierung im Editor bereit.
    Ermöglicht die Auswahl von Absatzformaten, Schriftarten, Schriftgrößen und Inline-Stilen.
    Die Werte werden über ein TextStyleDTO verwaltet.
    """

    def __init__(self, parent, paragraph_formats, text_style_dto, update_button_callback, export_button_callback):
        super().__init__(master=parent)

        self.grid(row=0, column=2, sticky='nsew', padx=15, pady=15)
        self._create_grid(4, 13)

        bold_font = Font(weight='bold', size=9)
        regular_font = Font(size=9)

        Label(self, text='Absatzformat', font=bold_font).grid(row=0, columnspan=4, sticky='w')
        paragraph_format_menu = OptionMenu(
            self,
            text_style_dto.paragraph_key,
            *paragraph_formats.style_presets.keys()
        )
        paragraph_format_menu.grid(row=1, column=0, columnspan=4, sticky='ew')

        Button(
            self,
            text='Absatzformat aktualisieren',
            command=update_button_callback
        ).grid(row=2, columnspan=4, sticky='ew')

        Label(self, text='Schrift', font=bold_font).grid(
            row=3, columnspan=4, sticky='w', pady=(25, 0)
        )
        OptionMenu(self, text_style_dto.family, *font.families()).grid(
            row=4, columnspan=3, sticky='ew'
        )

        OptionMenu(self, text_style_dto.size, *list(range(8, 42))).grid(
            row=4, column=3, sticky='ew'
        )

        Checkbutton(self, text='B', variable=text_style_dto.bold).grid(row=5, column=0, sticky='w')
        Checkbutton(self, text='I', variable=text_style_dto.italic).grid(row=5, column=1, sticky='w')
        Checkbutton(self, text='U', variable=text_style_dto.underline).grid(row=5, column=2, sticky='w')
        Checkbutton(self, text='H', variable=text_style_dto.highlight).grid(row=5, column=3, sticky='w')

        Entry(self, textvariable=text_style_dto.color, width=8).grid(
            row=6, columnspan=4, sticky='ew'
        )

        Label(self, text='Zeilenabstand', font=bold_font).grid(
            row=7, columnspan=4, sticky='w', pady=(25, 0)
        )
        Spinbox(
            self,
            from_=1,
            to=100,
            increment=1,
            textvariable=text_style_dto.line_height,
            width=3
        ).grid(row=8, columnspan=4, sticky='ew')

        Label(self, text='Abstand vor Absatz', font=regular_font).grid(
            row=9, columnspan=3, sticky='w'
        )
        Spinbox(
            self,
            from_=0,
            to=100,
            increment=1,
            textvariable=text_style_dto.space_before,
            width=3
        ).grid(row=9, column=3, sticky='ew')

        Label(self, text='Nach dem Absatz', font=regular_font).grid(
            row=10, columnspan=3, sticky='w'
        )
        Spinbox(
            self,
            from_=0,
            to=100,
            increment=1,
            textvariable=text_style_dto.space_after,
            width=3
        ).grid(row=10, column=3, sticky='ew')

        Label(self, text='Export', font=bold_font).grid(
            row=11, columnspan=4, sticky='w', pady=(25, 0)
        )
        Button(
            self,
            text='HTML exportieren',
            command=export_button_callback
        ).grid(row=12, columnspan=4, sticky='ew')

    def _create_grid(self, column, row):
        for i in range(column):
            self.grid_columnconfigure(i, weight=1)
        for i in range(row):
            self.grid_rowconfigure(i, weight=0)

