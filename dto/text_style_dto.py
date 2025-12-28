from tkinter import *
from tkinter.font import Font

from model.text_style import TextStyle

class TextStyleDto:
    """
    Repräsentiert ein DTO, das verwendet wird, um Stilwerte an andere Objekte weiterzugeben
    und gleichzeitig auf Änderungen über Traces zu reagieren.
    """

    def __init__(self, parent, paragraph_key, text_style):
        self.paragraph_key = StringVar(master=parent, value=paragraph_key)
        self.family = StringVar(master=parent, value=text_style.family)
        self.size = IntVar(master=parent, value=text_style.size)
        self.bold = BooleanVar(master=parent, value=text_style.bold)
        self.italic = BooleanVar(master=parent, value=text_style.italic)
        self.underline = BooleanVar(master=parent, value=text_style.underline)
        self.highlight = BooleanVar(master=parent, value=text_style.highlight)
        self.color = StringVar(master=parent, value=text_style.color)
        self.line_height = IntVar(master=parent, value=text_style.line_height)
        self.space_before = IntVar(master=parent, value=text_style.space_before)
        self.space_after = IntVar(master=parent, value=text_style.space_after)
        self.trace_break = False

    def set_paragraph_format_trace(self, callback):
        """
        Ermöglicht es, einen Trace für den paragraph_key zu setzen, der bei Änderungen
        die übergebene Callback-Funktion aufruft.
        :param callback: Eine Funktion, die aufgerufen wird, wenn sich der paragraph_key ändert.
        """
        self.paragraph_key.trace_add('write', callback)

    def set_inline_trace(self, callback):
        """
        Setzt für alle Stil-Variablen außer paragraph_key einen Trace, der bei Änderungen
        die übergebene Callback-Funktion aufruft.
        :param callback: Eine Funktion, die aufgerufen wird, wenn sich ein Stilwert ändert.
        """
        for var in self.__dict__.values():
            if isinstance(var, (StringVar, IntVar, BooleanVar, DoubleVar)) and var != self.paragraph_key:
                var.trace_add('write', callback)

    def set_text_style_dto(self, paragraph_key, text_style):
        """
        Setzt ein Flag, damit die Trace-Funktionen während der Aktualisierung nicht getriggert werden.
        Ohne dieses Flag würden die Trace-Funktionen bei jeder einzelnen Änderung ausgelöst werden.
        :param paragraph_key: Der neue paragraph_key, der verwendet werden soll.
        :param text_style: Der neue TextStyle, der verwendet werden soll.
        """
        self.trace_break = True
        self.paragraph_key.set(paragraph_key)
        self.family.set(text_style.family)
        self.size.set(text_style.size)
        self.bold.set(text_style.bold)
        self.italic.set(text_style.italic)
        self.underline.set(text_style.underline)
        self.highlight.set(text_style.highlight)
        self.color.set(text_style.color)
        self.line_height.set(text_style.line_height)
        self.space_before.set(text_style.space_before)
        self.space_after.set(text_style.space_after)
        self.trace_break = False

    def map_to_text_style(self):
        """
        Ermöglicht es, aus einem DTO ein TextStyle-Objekt zu erzeugen, um auf Funktionen von TextStyle zugreifen zu können.
        :return: Ein TextStyle-Objekt mit den aktuellen Werten des DTOs.
        """
        family = self.family.get()
        size = self.size.get()
        bold = self.bold.get()
        italic = self.italic.get()
        underline = self.underline.get()
        highlight = self.highlight.get()
        color = self.color.get()
        line_height = self.line_height.get()
        space_before = self.space_before.get()
        space_after = self.space_after.get()
        return TextStyle(family, size, bold, italic, underline, highlight, color, line_height, space_before, space_after)

    def map_to_dict(self):
        """
        Ermöglicht es, aus einem DTO ein dict zu erzeugen, welches als eine Kopie des DTOs dient.
        :return: Ein dict mit den aktuellen Werten des DTOs.
        """
        return {
            'paragraph_key': self.paragraph_key.get(),
            'family': self.family.get(),
            'size': self.size.get(),
            'bold': self.bold.get(),
            'italic': self.italic.get(),
            'underline': self.underline.get(),
            'highlight': self.highlight.get(),
            'color': self.color.get(),
            'line_height': self.line_height.get(),
            'space_before': self.space_before.get(),
            'space_after': self.space_after.get()
        }

    def map_to_text_style_dto(self, data: dict):
        """
        Ermöglicht es, mit einem dict das TextStyleDTO-Objekt anzupassen.
        Somit kann man anhand einer Kopie das TextStyleDTO-Objekt aktualisieren.
        :param data: Ein dict mit den Werten des TextStyleDTO-Objekts.
        """
        self.trace_break = True

        self.paragraph_key.set(data['paragraph_key'])
        self.family.set(data['family'])
        self.size.set(data['size'])
        self.bold.set(data['bold'])
        self.italic.set(data['italic'])
        self.underline.set(data['underline'])
        self.highlight.set(data['highlight'])
        self.color.set(data['color'])
        self.line_height.set(data['line_height'])
        self.space_before.set(data['space_before'])
        self.space_after.set(data['space_after'])

        self.trace_break = False

    def generate_font(self):
        """
        Generiert mit den aktuellen Parametern ein Font Objekt, welches verwendet werden kann, um einen tag zu erstellen.
        :return: Ein Font Objekt mit den aktuellen Parametern.
        """
        family = self.family.get()
        size = self.size.get()
        bold = 'bold' if self.bold.get() else 'normal'
        italic = 'italic' if self.italic.get() else 'roman'
        underline = self.underline.get()
        return Font(family=family, size=size, weight=bold, slant=italic, underline=underline)