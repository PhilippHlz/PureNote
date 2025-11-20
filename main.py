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
    my_text_widget = MyTextWidget(main_frame)
    # Event Bindings
    my_text_widget.text_widget.bind("<KeyPress>", lambda event: my_text_widget.on_key_pressed(event))
    my_text_widget.text_widget.bind("<Button-1>", lambda event: update_style_dropdown(my_text_widget.text_widget, font_style_var))

    # left frame
    left_frame = tk.Frame(root)
    left_frame.grid(column=0, row=0, sticky="nsew")


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