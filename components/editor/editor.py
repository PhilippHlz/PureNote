import tkinter as tk
from components.editor.font_style import FontStyle

FONT_STYLES = [FontStyle("p", "Verdana", 11, "normal", None),
               FontStyle("H1", "Verdana", 36, "bold", "#000000"),
               FontStyle("H2", "Verdana", 30, "bold", "#000000")]

class Editor(tk.Text):
    def __init__(self, master):
        super().__init__(master)
        self.current_style = tk.StringVar()
        self._initialize_styles()
        self.current_style.trace_add("write", self._change_paragraph_style)

        self.bind("<KeyRelease>", self._update_current_style_with_cursor)
        self.bind("<ButtonRelease-1>", self._update_current_style_with_cursor)

        self.bind("<KeyPress>", self._insert_char_with_current_style)

    def _initialize_styles(self):
        for index, font_style in enumerate(FONT_STYLES):
            font_style.create_font()

            if index == 0:
                self.current_style.set(font_style.name)

            self.tag_configure(font_style.name, font=font_style.font, foreground=font_style.color)


    def get_style_names(self):
        font_style_names = []
        for font_style in FONT_STYLES:
            font_style_names.append(font_style.name)
        return font_style_names

    def _remove_all_styles(self, start, end):
        for font_style in FONT_STYLES:
            self.tag_remove(font_style.name, start, end)

    def _change_paragraph_style(self, *args):
        cursor_index = self.index(tk.INSERT)

        start_nl = self.search(pattern="\n", index=cursor_index, backwards=True, stopindex="1.0")
        start = self.index(start_nl + "+1c") if start_nl else "1.0"

        end_nl = self.search(pattern="\n", index=cursor_index, stopindex=tk.END)
        end = end_nl if end_nl else tk.END

        self._remove_all_styles(start, end)
        self.tag_add(self.current_style.get(), start, end)


    def _update_current_style_with_cursor(self, event):
        left_cursor = self.index(tk.INSERT + "-1c")
        tags_at_index = self.tag_names(left_cursor)

        for font_style in FONT_STYLES:
            if font_style.name in tags_at_index:
                self.current_style.set(font_style.name)
                break

    def _insert_char_with_current_style(self, event):
        if len(event.char) == 0:
            return

        current_tag = self.current_style.get()
        self.insert(tk.INSERT, event.char, current_tag)
        return "break"

    #todo: zu add_inline_style mit remove inline_style umwandeln
    def highlight_selection(self, tag_name):
        try:
            start = self.index(tk.SEL_FIRST)
            end = self.index(tk.SEL_LAST)

            if self._check_tag_in_selection(tag_name):
                self.tag_remove(tag_name, start, end)
            else:
                self.tag_configure(tag_name, foreground="black", background="yellow")
                self.tag_add(tag_name, start, end)
                print("tag ist nicht vorhanden")

        except tk.TclError:
            pass

    def _check_tag_in_selection(self, tag_name):
        try:
            start = self.index(tk.SEL_FIRST)
            end = self.index(tk.SEL_LAST)

            while start < end:
                print(start)
                if tag_name not in self.tag_names(start):
                    return False
                start = self.index(start + "+1c")

            return True
        except tk.TclError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    editor = Editor(root)
    editor.pack()
    root.mainloop()