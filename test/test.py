import tkinter as tk
import tkinter.font as tk_font
from tkinter import TclError

X_PADDING = 25
Y_PADDING = 25
DEFAULT_FONT = "Verdana"
LIGHT_GREY = "#dadce0"
FONT_STYLE_OPTIONS = {"Normal text": [11, "normal", "#000000"], "H6": [11, "bold", "#000000"],
                      "H5": [17, "normal", "#000000"], "H4": [21, "bold", "#000000"], "H3": [25, "bold", "#000000"],
                      "H2": [30, "bold", "#000000"], "H1": [36, "bold", "#000000"], }

def main():
    # main window
    root = tk.Tk()
    root.title("PureNote")
    root.geometry("1200x800")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # global variables
    font_style_var = tk.StringVar(value=list(FONT_STYLE_OPTIONS.keys())[0])

    #main frame
    main_frame = tk.Frame(root)
    main_frame.grid(column=1, row=0, sticky="nsew")


    text_widget = tk.Text(main_frame, bg="white", fg="black", insertbackground="black", padx=X_PADDING, pady=Y_PADDING)
    text_widget.pack(fill="both", expand=True)
    text_widget.focus_set()

    # init text styles
    init_text_styles(text_widget, FONT_STYLE_OPTIONS, DEFAULT_FONT)
    # Event Bindings
    text_widget.bind("<KeyPress>", lambda event: on_key_pressed(event, text_widget, font_style_var))
    text_widget.bind("<Button-1>", lambda event: text_widget.after(1, lambda: update_style_dropdown(text_widget, font_style_var)))

    # left frame
    left_frame = tk.Frame(root)
    left_frame.grid(column=0, row=0, sticky="nsew")

    font_option_menu = tk.OptionMenu(left_frame, font_style_var, *FONT_STYLE_OPTIONS.keys(), command=lambda new_style_name: on_font_change(text_widget, new_style_name))
    font_option_menu.pack(fill="x", padx=X_PADDING, pady=(Y_PADDING, 0))

    # Button-Container mit linksbündiger Ausrichtung
    button_frame = tk.Frame(left_frame)
    button_frame.pack(fill="x", padx=X_PADDING)

    # Buttons mit fester Breite und linksbündiger Ausrichtung
    bold_font = tk_font.Font(family=DEFAULT_FONT, weight="bold")
    bold_option_button = tk.Button(button_frame, text="B", font=bold_font)
    bold_option_button.pack(side="left")

    italic_font = tk_font.Font(family=DEFAULT_FONT, slant="italic")
    italic_option_button = tk.Button(button_frame, text="I", font=italic_font)
    italic_option_button.pack(side="left")

    underline_font = tk_font.Font(family=DEFAULT_FONT, underline=True)
    underline_option_button = tk.Button(button_frame, text="U", font=underline_font)
    underline_option_button.pack(side="left")

    #right frame
    right_frame = tk.Frame(root, bg="green")
    right_frame.grid(column=2, row=0, sticky="nsew")

    root.mainloop()

def init_text_styles(text_widget, font_style_dict, font):
    for style, (size, weight, color) in font_style_dict.items():
        line_spacing = size * 0.35
        line_height = size * 0.2
        tag_font = tk_font.Font(family=font, size=size, weight=weight)

        if style == list(font_style_dict.keys())[0]:
            text_widget.tag_config(style, font=tag_font, foreground=color, spacing2=line_height)
        else:
            text_widget.tag_config(style, font=tag_font, foreground=color, spacing1=line_spacing, spacing2=line_height, spacing3=line_spacing)

def remove_all_tags(text_widget, start, end):
    for style in FONT_STYLE_OPTIONS.keys():
        text_widget.tag_remove(style, start, end)

def on_font_change(text_widget, new_style_name):
    try:
        start = text_widget.index("sel.first")
        end = text_widget.index("sel.last")
        remove_all_tags(text_widget, start, end)
        text_widget.tag_add(new_style_name, start, end)
    except TclError:
        pass

def apply_style_to_last_char(text_widget, style_name):
    try:
        cursor_pos = text_widget.index("insert")
        prev_pos = text_widget.index(f"{cursor_pos} - 1 char")
        remove_all_tags(text_widget, prev_pos, cursor_pos)
        text_widget.tag_add(style_name, prev_pos, cursor_pos)
    except TclError:
        pass

def on_key_pressed(event, text_widget, font_style_var):
    if event.char and len(event.char) == 1:
        current_style = font_style_var.get()
        text_widget.after_idle(lambda: apply_style_to_last_char(text_widget, current_style))

def update_style_dropdown(text_widget, font_style_var):
    try:
        cursor_pos = text_widget.index("insert")
        tags = text_widget.tag_names(cursor_pos)

        for style in FONT_STYLE_OPTIONS.keys ():
            if style in tags:
                font_style_var.set(style)
                return

        font_style_var.set("Normal text")
    except TclError:
        pass

if __name__ == "__main__":
    main()