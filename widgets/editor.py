from tkinter import *

class Editor(Text):
    """
    Diese Klasse erweitert das Tkinter Text Widget um die Fähigkeit,
    Absatz- und Inline-Stile zu verwalten und anzuwenden.
    Sie verwendet ein TextStyleDTO, um die aktuellen Stil-Eigenschaften zu speichern und anzuwenden.
    Die Stile werden als Tags im Text Widget verwaltet, wobei jeder Tag einem eindeutigen Token entspricht,
    der aus den Stil-Eigenschaften generiert wird.
    """
    def __init__(self, parent, paragraph_formats, text_style_dto):
        super().__init__(master=parent)
        self.paragraph_formats = paragraph_formats
        self.text_style_dto = text_style_dto

        # Speichert die generierten Tokens und deren zugehörigen TextStyles als dict
        self.token_cache = {}

        # Beinhaltet den aktuellen Token der für tags verwendet wird
        self.current_token = None
        self.set_current_token()

        # bindings

        # Zeichen einfügen
        self.bind('<KeyPress>', self._insert_char)

        # Wenn mit der Maus durch den Text navigiert wird durch Klicken ändert sich der Stil
        self.bind('<ButtonRelease-1>', self._change_text_style_with_cursor)
        
        # Wenn mit den Pfeiltasten durch den Text navigiert wird ändert sich der Stil
        self.bind('<KeyRelease-Left>', self._change_text_style_with_cursor)
        self.bind('<KeyRelease-Right>', self._change_text_style_with_cursor)
        self.bind('<KeyRelease-Up>', self._change_text_style_with_cursor)
        self.bind('<KeyRelease-Down>', self._change_text_style_with_cursor)

        # Beim drücken von Return/Enter wird Stil zurück auf 'p' gesetzt
        self.bind('<KeyRelease-Return>', self._change_to_paragraph)

        self.grid(row=0, column=1, sticky='nsew')
        self.configure(background='white')
        self.focus()
        self.config(insertbackground='black')

    def _insert_char(self, event):
        """
        Ermöglicht es, ein Zeichen oder eine Ziffer in den Text einzufügen.
        Wenn das Zeichen nicht printable ist, wird das Standardverhalten ausgeführt.
        Wenn Return, Backspace, Left, Right, Up oder Down gedrückt wird, wird das Standardverhalten ausgeführt.
        :param event: Event mit Key-Input
        """
        if event.keysym in ('Return', 'BackSpace', 'Left', 'Right', 'Up', 'Down'):
            return None

        if event.char.isprintable():

            self.insert(INSERT, event.char, self.current_token)
            return 'break'

        return None

    def set_current_token(self):
        """
        Setzt das aktuelle Token anhand des aktuellen TextstyleDTOs.
        Wenn das Token nicht im Token-Cache enthalten ist, wird ein passender Tag generiert und im Token-Cache gespeichert.
        Der Token-Cache verwendet den Token als Key und das TextStyleDto als dict Value.
        Somit kann man über den Token schnell den zugehörigen TextStyle finden mit allen Parametern und diesen anwenden.
        """
        self.current_token = self.text_style_dto.map_to_text_style().generate_token()

        if self.current_token in self.token_cache:
            return

        # Tag wird mit allen Parametern aus dem TextStyleDTO generiert dazu gehören der Token, die Schriftart, Farbe, Zeilenhöhe und Abstände.
        self._generate_tag()
        self.token_cache[self.current_token] = self.text_style_dto.map_to_dict()
        return

    def apply_style_to_line(self):
        """
        Wird ausgelöst, wenn sich das Absatzformat ändert.
        Setzt eine komplette Zeile mit dem aktuellen Token.
        Es werden alle alten Tags aus der Zeile entfernt und der aktuelle Token hinzugefügt.
        Wird verwendet, wenn das Absatzformat geändert wird.
        """
        line_start = self.index('insert linestart -1c') #-1c, weil sonst der Zeilenanfang den tag der vorherigen Zeile übernimmt
        line_end = self.index('insert lineend')

        for token in self.token_cache:
            self.tag_remove(token, line_start, line_end)

        self.tag_add(self.current_token, line_start, line_end)

    def apply_style_to_selection(self):
        """
        Versucht eine Text-Selektion zu finden, wenn keine gefunden wird passiert nichts.
        Wenn eine Selektion gefunden wurde, werden alle alten Tags aus der Selektion entfernt und der aktuelle Token hinzugefügt.
        Wird verwendet, wenn der Inline-Stil geändert wird.
        """
        try:
            selection_start = self.index(SEL_FIRST)
            selection_end = self.index(SEL_LAST)

            for token in self.token_cache:
                self.tag_remove(token, selection_start, selection_end)

            self.tag_add(self.current_token, selection_start, selection_end)

        except TclError:
            pass

    def update_preset_style(self):
        """
        Wird verwendet, wenn das Absatzformat Absatzformat aktualisieren Button geklickt wird.
        Ermittelt anhand des text_style_dto paragraph_key den alten Token und vergleicht diesen mit dem aktuellen Token.
        Wenn sich der Token geändert hat, werden alle Vorkommen des alten Tokens im Text durch den aktuellen Token ersetzt.
        Abschließend wird das neue TextStyle im paragraph_formats als preset gespeichert.
        """
        paragraph_key = self.text_style_dto.paragraph_key.get()
        old_token = self.paragraph_formats.get_style_preset(paragraph_key).generate_token()
        if old_token == self.current_token:
            return

        # tag_ranges gibt eine Liste von Start- und End-Indexen (Start1, End1, Start2, End2, ...) zurück, daher wird in 2er Schritten iteriert.
        tag_ranges_old_token = self.tag_ranges(old_token)
        for i in range(0, len(tag_ranges_old_token), 2):
            self.tag_remove(old_token, tag_ranges_old_token[i], tag_ranges_old_token[i+1])
            self.tag_add(self.current_token, tag_ranges_old_token[i], tag_ranges_old_token[i+1])

        self.paragraph_formats.set_style_preset(paragraph_key, self.text_style_dto.map_to_text_style())

    def highlight_selection(self, tag, color):
        """
        Versucht eine Text-Selektion zu finden, wenn keine gefunden wird passiert nichts.
        Wenn eine Selektion gefunden wurde, wird ein Hintergrund mit dem angegebenen color auf die Selektion angewendet.
        Der Name des Tags ist der title der To-Do Aufgabe.
        Wird verwendet, wenn eine To-Do Aufgabe hinzugefügt wird, um den Text im Editor hervorzuheben mit der passenden To-Do-Farbe.
        """
        try:
            start = self.index(SEL_FIRST)
            end = self.index(SEL_LAST)

            self.tag_configure(tag, background=color)
            self.tag_add(tag, start, end)
        except TclError:
            pass

    def remove_tag(self, tag):
        """
        Entfernt einen definierten Tag aus dem gesamten Text.
        Wird verwendet wenn eine To-Do Task gelöscht wird.
        """
        self.tag_remove(tag, '1.0', 'end')

    def _change_text_style_with_cursor(self, _):
        """
        Wird ausgelöst, wenn mit der Maus oder den Pfeiltasten durch den Text navigiert wird.
        Nimmt den Tag des linken Cursors und sucht den passenden TextStyle im Token-Cache.
        Wenn der Tag gefunden wird, wird der TextStyleDTO aktualisiert.
        ToDo: Wenn in die Mitte eines Tasks geklickt wird sollte in diesem Still weiter geschrieben werden (mit Hintergrund).
        ToDo: Oder ganzen Absatz einfärben
        """
        last_cursor_pos = self.index(INSERT + '-1c')
        tags_at_last_cursor_pos = self.tag_names(last_cursor_pos)

        for tag in tags_at_last_cursor_pos:
            if tag in self.token_cache:
                self.current_token = tag
                self.text_style_dto.map_to_text_style_dto(self.token_cache[tag])
                return

    def _change_to_paragraph(self, _):
        """
        Wird ausgelöst, wenn Return gedrückt wird.
        Wenn der paragraph_key nicht 'p' ist, wird der paragraph_key auf 'p' gesetzt und der TextStyleDTO aktualisiert.
        """
        if self.text_style_dto.paragraph_key.get() != 'p':
            self.text_style_dto.set_text_style_dto('p', self.paragraph_formats.get_style_preset('p'))
            self.set_current_token()
            self.apply_style_to_line()
        return

    def _generate_tag(self):
        """
        Generiert einen Tag mit den aktuellen TextStyle-Werten.
        """
        token = self.current_token
        tag_font = self.text_style_dto.generate_font()

        tag_color = self.text_style_dto.color.get()
        tag_background = 'yellow' if self.text_style_dto.highlight.get() else None
        line_height = self.text_style_dto.line_height.get()
        space_before = self.text_style_dto.space_before.get()
        space_after = self.text_style_dto.space_after.get()
        try:
            self.tag_configure(token, font=tag_font, foreground=tag_color, spacing1=space_before, spacing2=line_height, spacing3=space_after, background=tag_background)
        except TclError:
            pass