import tkinter as tk
from tkinter import filedialog
import os
import sys
import subprocess


class MusicPlayer(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f3f4f6")

        self.file_path = None

        tk.Label(self, text="Musikplayer", font=("Arial", 9, "bold"), bg="#f3f4f6")\
            .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 3))

        tk.Button(self, text="Datei", font=("Arial", 8), width=8,
                  command=self.choose_file)\
            .grid(row=1, column=0, sticky="w")

        tk.Button(self, text="Play", font=("Arial", 8), width=8,
                  command=self.play_file)\
            .grid(row=1, column=1, sticky="w", padx=(4, 0))

        self.file_label = tk.Label(self, text="", font=("Arial", 7), bg="#f3f4f6")
        self.file_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(3, 0))

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

    def choose_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Audio-Dateien", "*.mp3 *.wav *.ogg *.flac"),
                ("Alle Dateien", "*.*")
            ]
        )
        if path:
            self.file_path = path
            self.file_label.config(text=os.path.basename(path))

    def play_file(self):
        if not self.file_path:
            return

        if sys.platform.startswith("win"):
            os.startfile(self.file_path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", self.file_path])
        else:
            subprocess.Popen(["xdg-open", self.file_path])
