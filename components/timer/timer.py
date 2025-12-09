import tkinter as tk

class Timer(tk.Frame):
    WORK_PHASE = "WORK"
    BREAK_PHASE = "BREAK"

    def __init__(self, master, work_time, break_time):
        super().__init__(master)

        self.work_time = work_time * 60
        self.break_time = break_time * 60

        self.remaining_work_time = self.work_time
        self.remaining_break_time = self.break_time

        self.running = False
        self.phase = self.WORK_PHASE
        self.active_after = None

        self.remaining_time_label = tk.Label(self, text=self._format_time(self.remaining_work_time))
        self.remaining_time_label.pack()

        self.start_stop_button = tk.Button(self, text="Start", command=self._toggle_timer)
        self.start_stop_button.pack()

    def _toggle_timer(self):
        if not self.running:
            self.running = True
            self.start_stop_button.config(text="Pause")
            self._countdown()
        else:
            self.running = False
            self.start_stop_button.config(text="Start")
            if self.active_after:
                self.after_cancel(self.active_after)
                self.active_after = None

    def _countdown(self):
        if self.phase == self.WORK_PHASE:
            remaining_time = self.remaining_work_time
        else:
            remaining_time = self.remaining_break_time

        if remaining_time == 0:
            self._switch_phase()
            return

        if self.phase == self.WORK_PHASE:
            self.remaining_work_time -= 1
            self.remaining_time_label.config(text=self._format_time(self.remaining_work_time))
        else:
            self.remaining_break_time -= 1
            self.remaining_time_label.config(text=self._format_time(self.remaining_break_time))

        self.active_after = self.after(1000, self._countdown)

    def _switch_phase(self):
        if self.phase == self.WORK_PHASE:
            self.phase = self.BREAK_PHASE
            self.remaining_break_time = self.break_time
            self.remaining_time_label.config(text=self._format_time(self.remaining_break_time))
        else:
            self.phase = self.WORK_PHASE
            self.remaining_work_time = self.work_time
            self.remaining_time_label.config(text=self._format_time(self.remaining_work_time))

        if self.running:
            self._countdown()

    @staticmethod
    def _format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Timer")
    root.geometry("400x200")
    timer = Timer(root, work_time=1, break_time=2)
    timer.pack()

    root.mainloop()