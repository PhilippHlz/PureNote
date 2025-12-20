import tkinter as tk
from components.todo.task import Task

class TodoList(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.task_data = []
        self.title_input = None
        self.title_input_content = tk.StringVar()
        self.submit_button = None
        self.description_input = None
        self._render_input_fields()

    #todo: Style hinzufügen
    def _render_input_fields(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x")

        title_label = tk.Label(top_frame, text="Title")
        title_label.pack()

        title_input = tk.Entry(top_frame, textvariable=self.title_input_content)
        title_input.pack(fill="x")

        self.description_input = tk.Entry(top_frame)
        self.description_input.pack(fill="x")

        self.submit_button = tk.Button(top_frame, text="Submit", command=self._on_create_task)
        self.submit_button.pack()
        self.submit_button.config(state="disabled")

        self.title_input_content.trace_add("write", self._disable_submit_button)

    def add_task(self, title, description):
        task = Task(self, title, description, tk.BooleanVar())
        task.check_status.trace_add("write", lambda *args: self._delete_task())
        task.render()
        self.task_data.append(task)

    def _delete_task(self, *args):
        for task in self.task_data:
            if task.check_status.get():
                self.task_data.remove(task)
                task.destroy()
                print(self.task_data)

    def _on_create_task(self):
        title = self.title_input_content.get()
        description = self.description_input.get()
        self.add_task(title, description)
        self._clear_inputs()

    def _disable_submit_button(self, *args):
        if self.title_input_content.get() == "":
            self.submit_button.config(state="disabled")
        else:
            self.submit_button.config(state="normal")

    def _clear_inputs(self):
        self.title_input_content.set("")
        self.description_input.delete(0, "end")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Todo List")
    root.geometry("400x200")
    todo_list = TodoList(root)
    todo_list.pack(fill="both", expand=True)
    root.mainloop()