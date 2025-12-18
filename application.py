from tkinter import *
from tkinter import font
from tkinter.font import Font

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title('The Pure Note Project')
        self.geometry('800x600')

        # layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # data
        self.paragraph_formats = ParagraphFormats()
        self.current_style = CurrentStyle(self, 'p', self.paragraph_formats.get_style_preset('p'))
        self.current_style.set_paragraph_format_trace(self._on_paragraph_format_change)
        self.current_style.set_inline_format_trace(self._on_inline_format_change)

        # widgets
        EditorMenu(self, self.paragraph_formats, self.current_style, self._on_update)
        self.editor = Editor(self, self.paragraph_formats, self.current_style)

    def _on_paragraph_format_change(self, *_):
        if self.current_style.trace_flag:
            return
        key = self.current_style.paragraph_format.get()
        preset = self.paragraph_formats.get_style_preset(key)
        self.current_style.set_current_style(key, preset)

        self.editor.set_current_style()
        self.editor.change_paragraph_style()
        self.current_style.print_all()

    def _on_inline_format_change(self, *_):
        if self.current_style.trace_flag:
            return
        self.editor.set_current_style()
        self.editor.apply_style_to_selection()
        print('test')

    def _on_update(self, *_):
        self.editor.update_style()


class EditorMenu(Frame):
    def __init__(self, parent, paragraph_formats, current_style, on_update):
        super().__init__(master=parent)
        self.paragraph_formats = paragraph_formats
        self.current_style = current_style
        self.on_update = on_update
        paragraph_format_keys = paragraph_formats.style_presets.keys()

        self.grid(row=0, column=1, sticky='nsew')

        paragraph_option_menu = OptionMenu(self, self.current_style.paragraph_format, *paragraph_format_keys)
        paragraph_option_menu.pack(side='left')

        font_family_menu = OptionMenu(self, self.current_style.family, *font.families())
        font_family_menu.pack(side='left')

        font_size_menu = OptionMenu(self, self.current_style.size, *list(range(8, 42)))
        font_size_menu.pack(side='left')

        bold_checkbutton = Checkbutton(self, text='Bold', variable=self.current_style.bold)
        bold_checkbutton.pack(side='left')

        italic_checkbutton = Checkbutton(self, text='Italic', variable=self.current_style.italic)
        italic_checkbutton.pack(side='left')

        underline_checkbutton = Checkbutton(self, text='Underline', variable=self.current_style.underline)
        underline_checkbutton.pack(side='left')

        highlight_checkbutton = Checkbutton(self, text='Highlight', variable=self.current_style.highlight)
        highlight_checkbutton.pack(side='left')

        color_entry = Entry(self, textvariable=self.current_style.color)
        color_entry.pack(side='left')

        update_button = Button(self, text='Update', command=self.on_update)
        update_button.pack(side='right')

class Editor(Text):
    def __init__(self, parent, paragraph_formats, current_style):
        super().__init__(master=parent)
        self.paragraph_formats = paragraph_formats
        self.current_style = current_style
        self.font_cache = {}
        self.current_style_token = self.set_current_style()
        self.focus_set()
        #self.debug_print_current_style_tag()


        self.grid(row=1, column=1, sticky='nsew')

        self.bind('<KeyPress>', self._insert_char)
        self.bind('<ButtonRelease-1>', self._change_current_style_with_cursor)
        self.bind('<KeyRelease-Left>', self._change_current_style_with_cursor)
        self.bind('<KeyRelease-Right>', self._change_current_style_with_cursor)
        self.bind('<KeyRelease-Up>', self._change_current_style_with_cursor)
        self.bind('<KeyRelease-Down>', self._change_current_style_with_cursor)
        self.bind('<Return>', self.change_to_paragraph)

    def _insert_char(self, event):
        if not event.char.isalpha():
            return None
        self.insert('insert', event.char, self.current_style_token)
        return 'break'

    def set_current_style(self):
        tag_token = self.current_style.generate_token()
        self.current_style_token = tag_token

        if tag_token in self.font_cache:
            return tag_token

        tag_font = self.generate_font()
        text_color = self.current_style.color.get()

        self.font_cache[tag_token] = self.current_style.make_snapshot()
        self.tag_configure(tag_token, font=tag_font, foreground=text_color)
        return tag_token

    def generate_font(self):
        return Font(family=self.current_style.family.get(), size=self.current_style.size.get(),
                    weight='bold' if self.current_style.bold.get() else 'normal',
                    slant='italic' if self.current_style.italic.get() else 'roman',
                    underline=self.current_style.underline.get(), overstrike=self.current_style.highlight.get())

    def change_paragraph_style(self):
        print('test')
        print(self.current_style_token)
        start = self.index('insert linestart')
        end = self.index('insert lineend')

        for tag in self.tag_names():
            self.tag_remove(tag, start, end)

        self.tag_add(self.current_style_token, start, end)
        print(self.tag_names(start))

    def _change_current_style_with_cursor(self, _):
        last_cursor_pos = self.index(INSERT + '-1c')
        tag_names = self.tag_names(last_cursor_pos)
        print(self.current_style_token)

        for tag in tag_names:
            if tag in self.font_cache:
                self.current_style_token = tag
                self.current_style.apply_snapshot(self.font_cache[tag])
                return

    def apply_style_to_selection(self):
        try:
            start = self.index(SEL_FIRST)
            end = self.index(SEL_LAST)

            tag_token = self.current_style.generate_token()

            for old_tag in self.font_cache.keys():
                self.tag_remove(old_tag, start, end)

            self.tag_add(tag_token, start, end)

        except TclError:
            pass

    def update_style(self):
        old_preset = self.is_paragraph_preset()
        if old_preset:
            tag_ranges = self.tag_ranges(old_preset)
            for i in range(0, len(tag_ranges), 2):
                self.tag_remove(old_preset, tag_ranges[i], tag_ranges[i + 1])
                self.tag_add(self.current_style_token, tag_ranges[i], tag_ranges[i + 1])

    def is_paragraph_preset(self):
        current_key = self.current_style.paragraph_format.get()
        old_token = self.paragraph_formats.style_presets[current_key].generate_token()
        if old_token == self.current_style_token:
            return None


        self.paragraph_formats.set_style_preset(current_key, self.current_style.map_to_textstyle())

        self.paragraph_formats.token_map[current_key] = self.paragraph_formats.style_presets[
            current_key].generate_token()

        return old_token

    def change_to_paragraph(self, _):
        if self.current_style.paragraph_format.get() == 'p':
            return
        
        self.current_style.set_current_style('p', self.paragraph_formats.get_style_preset('p'))
        self.set_current_style()
class TextStyle:
    def __init__(self, family: str, size: int, bold: bool, italic: bool, underline: bool, highlight: bool, color: str):
        self.family: str = family
        self.size: int = size
        self.bold: bool = bold
        self.italic: bool = italic
        self.underline: bool = underline
        self.highlight: bool = highlight
        self.color: str = color

    def generate_token(self):
        return f'{self.family}_{self.size}_{self.bold}_{self.italic}_{self.underline}_{self.highlight}_{self.color}'


class ParagraphFormats:
    def __init__(self):
        self.style_presets: dict[str, TextStyle] = {
            'p': TextStyle('Arial', 12, False, False, False, False, '#333333'),
            'h1': TextStyle('Arial', 36, True, False, False, False, '#333333'),
            'h2': TextStyle('Arial', 30, True, False, False, False, '#333333'),
            'h3': TextStyle('Arial', 24, True, False, False, False, '#333333'),
            'h4': TextStyle('Arial', 20, True, False, False, False, '#333333'),
            'h5': TextStyle('Arial', 17, False, False, False, False, '#333333'),
            'h6': TextStyle('Arial', 14, False, False, False, False, '#333333'),
        }
        self.token_map = self.generate_token_list()

    def get_style_preset(self, style_key: str) -> TextStyle:
        return self.style_presets[style_key]

    def set_style_preset(self, style_key: str, textstyle: TextStyle):
        self.style_presets[style_key] = textstyle

    def generate_token_list(self):
        tokens = {}
        for key, value in self.style_presets.items():
            tokens[key] = value.generate_token()
        return tokens


class CurrentStyle:
    def __init__(self, parent, key: str, text_style: TextStyle):
        self.paragraph_format = StringVar(master=parent, value=key)
        self.family = StringVar(master=parent, value=text_style.family)
        self.size = IntVar(master=parent, value=text_style.size)
        self.bold = BooleanVar(master=parent, value=text_style.bold)
        self.italic = BooleanVar(master=parent, value=text_style.italic)
        self.underline = BooleanVar(master=parent, value=text_style.underline)
        self.highlight = BooleanVar(master=parent, value=text_style.highlight)
        self.color = StringVar(master=parent, value=text_style.color)

        self.trace_flag = False

    def set_paragraph_format_trace(self, callback):
        self.paragraph_format.trace_add('write', callback)

    def set_inline_format_trace(self, callback):
        for var in self.__dict__.values():
            if hasattr(var, 'trace_add') and var != self.paragraph_format:
                var.trace_add('write', callback)


    def set_current_style(self, key: str, textstyle: TextStyle):
        self.trace_flag = True

        self.paragraph_format.set(key)
        self.family.set(textstyle.family)
        self.size.set(textstyle.size)
        self.bold.set(textstyle.bold)
        self.italic.set(textstyle.italic)
        self.underline.set(textstyle.underline)
        self.highlight.set(textstyle.highlight)
        self.color.set(textstyle.color)

        self.trace_flag = False

    def map_to_textstyle(self) -> TextStyle:
        return TextStyle(
            self.family.get(),
            int(self.size.get()),
            self.bold.get(),
            self.italic.get(),
            self.underline.get(),
            self.highlight.get(),
            self.color.get()
        )

    def print_all(self):
        for var in self.__dict__.values():
            if hasattr(var, 'trace_add'):
                print(var.get())

    def generate_token(self) -> str:
        return (
            f'{self.family.get()}_{self.size.get()}_'
            f'{self.bold.get()}_{self.italic.get()}_{self.underline.get()}_'
            f'{self.highlight.get()}_{self.color.get()}'
        )

    def make_snapshot(self):
        return {
            'paragraph_format': self.paragraph_format.get(),
            'family': self.family.get(),
            'size': self.size.get(),
            'bold': self.bold.get(),
            'italic': self.italic.get(),
            'underline': self.underline.get(),
            'highlight': self.highlight.get(),
            'color': self.color.get()
        }

    def apply_snapshot(self, snap):
        self.trace_flag = True
        try:
            self.paragraph_format.set(snap['paragraph_format'])
            self.family.set(snap['family'])
            self.size.set(snap['size'])
            self.bold.set(snap['bold'])
            self.italic.set(snap['italic'])
            self.underline.set(snap['underline'])
            self.highlight.set(snap['highlight'])
            self.color.set(snap['color'])
        finally:
            self.trace_flag = False

if __name__ == '__main__':
    app = Application()
    app.mainloop()
