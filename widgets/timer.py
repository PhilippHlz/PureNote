import tkinter as tk
from tkinter import messagebox


class Timer(tk.Frame):
    WORK_PHASE = "WORK"
    BREAK_PHASE = "BREAK"

    def __init__(self, master, work_time=30, break_time=5):
        super().__init__(master)

        # ===== State =====
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

        # ===== UI (kompakt, zieht den linken Panel nicht auseinander) =====
        # Alles wird links ausgerichtet, damit es optisch "ruhig" bleibt.
        settings = tk.Frame(self)
        settings.pack(anchor="w", fill="x", padx=10, pady=(6, 4))

        tk.Label(settings, text="Fokus (Min):").grid(row=0, column=0, sticky="w")
        tk.Spinbox(settings, from_=1, to=120, width=4, textvariable=self.work_minutes).grid(
            row=0, column=1, sticky="w", padx=(6, 12)
        )

        tk.Label(settings, text="Pause (Min):").grid(row=0, column=2, sticky="w")
        tk.Spinbox(settings, from_=1, to=60, width=4, textvariable=self.break_minutes).grid(
            row=0, column=3, sticky="w", padx=(6, 0)
        )

        self.phase_label = tk.Label(self, font=("Arial", 12, "bold"))
        self.phase_label.pack(anchor="w", padx=10, pady=(0, 4))

        self.remaining_time_label = tk.Label(self, font=("Arial", 20))
        self.remaining_time_label.pack(anchor="w", padx=10, pady=(0, 6))

        # Buttons: outer frame füllt Breite, inner frame ist automatisch mittig
        button_outer = tk.Frame(self)
        button_outer.pack(fill="x", padx=10, pady=(0, 8))

        button_frame = tk.Frame(button_outer)
        button_frame.pack()  # zentriert

        self.start_stop_button = tk.Button(button_frame, text="Start", width=8, command=self._toggle_timer)
        self.start_stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", width=8, command=self._reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self._reset_timer()

    def _apply_settings(self):
        self.work_time = int(self.work_minutes.get()) * 60
        self.break_time = int(self.break_minutes.get()) * 60
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
        remaining = self.remaining_work_time if self.phase == self.WORK_PHASE else self.remaining_break_time

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
            self.active_after = None

        self.running = False
        self.phase = self.WORK_PHASE
        self.is_fresh_start = True

        self._apply_settings()
        self.start_stop_button.config(text="Start")
        self._update_ui()

    def _update_ui(self):
        if self.phase == self.WORK_PHASE:
            self.phase_label.config(text="Fokuszeit", fg="green")
            self.remaining_time_label.config(text=self._format_time(self.remaining_work_time))
        else:
            self.phase_label.config(text="Pause", fg="blue")
            self.remaining_time_label.config(text=self._format_time(self.remaining_break_time))

    @staticmethod
    def _format_time(seconds):
        return f"{seconds // 60:02}:{seconds % 60:02}"

