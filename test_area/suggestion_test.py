import tkinter as tk


def read_txt_file(dateiname):
    try:
        with open(dateiname, 'r') as f:
            return [zeile.strip() for zeile in f.readlines()]
    except FileNotFoundError:
        print('error')


class Suggestion:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x200")

        self.suggestion_frame = tk.Frame(root)
        self.suggestion_frame.pack()

        self.var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.var)
        self.entry.pack()
        self.var.trace_add("write", self.on_text_changed)

        self.suggestions = []
        self.suggestion_labels = []

        self.wordlist = read_txt_file("wordlist-german.txt") #evtl. zu SQLLite -> auf Git gibt es auch liste mit 60.000 Wörtern

    def clear_suggestions(self):
        for label in self.suggestion_labels:
            label.destroy()
        self.suggestion_labels = []

    def on_text_changed(self, *args):
        current_text = self.var.get()
        self.clear_suggestions()

        #Evtl. machen das die ersten 5 oder 10 vorschläge angezeigt werden
        if len(current_text) > 2:
            matching_words = []
            for word in self.wordlist:
                if word.lower().startswith(current_text):
                    matching_words.append(word)



            for word in matching_words:
                label = tk.Label(self.suggestion_frame,text=word,)
                label.pack()
                self.suggestion_labels.append(label)


if __name__ == "__main__":
    root = tk.Tk()
    app = Suggestion(root)
    root.mainloop()