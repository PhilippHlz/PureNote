import tkinter as tk
from tkinter import messagebox


class Timer(tk.Frame):
    WORK_PHASE = "WORK"
    BREAK_PHASE = "BREAK"

    def __init__(self, master, work_time, break_time):
        super().__init__(master)

        self.work_minutes = tk.IntVar(value=work_time)
        self.break_minutes = tk.IntVar(value=break_time)

        self.work_time = work_time * 60
        self.break_time = break_time * 60

        self.remaining_work_time = self.work_time
        self.remaining_break_time = self.break_time

        self.running = False
        self.phase = self.WORK_PHASE
        self.active_after = None
        self.is_fresh_start = True

     
        settings = tk.Frame(self)
        settings.pack(pady=5)

        tk.Label(settings, text="Fokus (Min):").grid(row=0, column=0)
        tk.Spinbox(
            settings,
            from_=1,
            to=120,
            width=5,
            textvariable=self.work_minutes
        ).grid(row=0, column=1)

        tk.Label(settings, text="Pause (Min):").grid(row=0, column=2)
        tk.Spinbox(
            settings,
            from_=1,
            to=60,
            width=5,
            textvariable=self.break_minutes
        ).grid(row=0, column=3)

       
        self.phase_label = tk.Label(self, font=("Arial", 14, "bold"))
        self.phase_label.pack(pady=5)

        self.remaining_time_label = tk.Label(self, font=("Arial", 24))
        self.remaining_time_label.pack(pady=5)

    
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        self.start_stop_button = tk.Button(
            button_frame,
            text="Start",
            width=8,
            command=self._toggle_timer
        )
        self.start_stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            width=8,
            command=self._reset_timer
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self._reset_timer()

    def _apply_settings(self):
        self.work_time = self.work_minutes.get() * 60
        self.break_time = self.break_minutes.get() * 60
        self.remaining_work_time = self.work_time
        self.remaining_break_time = self.break_time

    def _toggle_timer(self):
        if not self.running:
            if self.is_fresh_start:
                self._apply_settings()
                self.is_fresh_start = False

            self.running = True
            self.start_stop_button.config(text="Pause")
            self._update_ui()
            self._countdown()
        else:
            self.running = False
            self.start_stop_button.config(text="Start")
            self._update_ui()
            if self.active_after:
                self.after_cancel(self.active_after)
                self.active_after = None

    def _countdown(self):
        remaining = (
            self.remaining_work_time
            if self.phase == self.WORK_PHASE
            else self.remaining_break_time
        )

        if remaining <= 0:
            self._on_phase_finished()
            return

        if self.phase == self.WORK_PHASE:
            self.remaining_work_time -= 1
        else:
            self.remaining_break_time -= 1

        self._update_ui()
        self.active_after = self.after(1000, self._countdown)

    def _on_phase_finished(self):
        if self.phase == self.WORK_PHASE:
            messagebox.showinfo("Timer", "Fokuszeit beendet. Pause startet.")
            self.phase = self.BREAK_PHASE
            self.remaining_break_time = self.break_time
        else:
            messagebox.showinfo("Timer", "Pause beendet. Neue Fokuszeit startet.")
            self.phase = self.WORK_PHASE
            self.remaining_work_time = self.work_time

        self._update_ui()
        if self.running:
            self._countdown()

    def _reset_timer(self):
        if self.active_after:
            self.after_cancel(self.active_after)

        self.running = False
        self.phase = self.WORK_PHASE
        self.is_fresh_start = True

        self._apply_settings()
        self.start_stop_button.config(text="Start")
        self._update_ui()

    def _update_ui(self):
        if self.running:
            if self.phase == self.WORK_PHASE:
                self.phase_label.config(text="Fokuszeit", fg="green")
            else:
                self.phase_label.config(text="Pause", fg="blue")
        else:
            self.phase_label.config(text="Pause", fg="blue")

        if self.phase == self.WORK_PHASE:
            self.remaining_time_label.config(
                text=self._format_time(self.remaining_work_time)
            )
        else:
            self.remaining_time_label.config(
                text=self._format_time(self.remaining_break_time)
            )

    @staticmethod
    def _format_time(seconds):
        return f"{seconds // 60:02}:{seconds % 60:02}"
