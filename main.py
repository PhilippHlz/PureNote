import tkinter as tk
from components.editor.editor import Editor
from components.timer.timer import Timer
from components.todo.task_dto import TodoList
from components.export.html_exporter import export_editor_to_html
from pathlib import Path


def main():
    root = tk.Tk()
    root.title("Pure Note")
    root.geometry("1000x900")

    editor = Editor(root)
    editor.pack(fill=tk.BOTH, expand=True)

    font_option_menu = tk.OptionMenu(
        root,
        editor.current_style,
        *editor.get_style_names()
    )
    font_option_menu.pack()

    highlight_button = tk.Button(
        root,
        text="Highlight",
        command=lambda: editor.highlight_selection("markierung")
    )
    highlight_button.pack()

    export_button = tk.Button(
        root,
        text="Export HTML",
        command=lambda: export_editor_to_html(
            editor,
            filename=str(Path(__file__).resolve().parent / "export.html")
        )
    )
    export_button.pack()

    todo_list = TodoList(root)
    todo_list.pack(fill=tk.X)

    timer = Timer(root, 30, 5)
    timer.pack()

    root.mainloop()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
