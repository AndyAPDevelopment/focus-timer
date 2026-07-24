import customtkinter as ctk
from core.timer import FocusTimer
from core.logger import SessionLogger

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FocusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Focus Timer")
        self.geometry("380x520")
        self.resizable(False, False)

        self.timer = FocusTimer(25)
        self.logger = SessionLogger()
        self.timer.on_tick = self._update_display
        self.timer.on_finish = self._on_timer_finish

        self._build_ui()
        self._update_stats()

    def _build_ui(self):
        # Title
        ctk.CTkLabel(self, text="Focus Timer", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(20, 10))

        # Timer display
        self.time_label = ctk.CTkLabel(self, text="25:00", font=ctk.CTkFont(size=48, weight="bold"))
        self.time_label.pack(pady=10)

        # Duration selector
        duration_frame = ctk.CTkFrame(self, fg_color="transparent")
        duration_frame.pack(pady=5)

        ctk.CTkLabel(duration_frame, text="Minutes:").pack(side="left", padx=5)
        self.duration_var = ctk.StringVar(value="25")
        self.duration_entry = ctk.CTkEntry(duration_frame, width=60, textvariable=self.duration_var)
        self.duration_entry.pack(side="left")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)

        self.start_btn = ctk.CTkButton(btn_frame, text="Start", width=90, command=self._start)
        self.start_btn.pack(side="left", padx=5)

        self.pause_btn = ctk.CTkButton(btn_frame, text="Pause", width=90, command=self._pause, state="disabled")
        self.pause_btn.pack(side="left", padx=5)

        self.reset_btn = ctk.CTkButton(btn_frame, text="Reset", width=90, command=self._reset)
        self.reset_btn.pack(side="left", padx=5)

        # Log section
        ctk.CTkLabel(self, text="Log this session", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))

        self.note_entry = ctk.CTkEntry(self, placeholder_text="Optional note (e.g. deep work, coding...)", width=300)
        self.note_entry.pack(pady=5)

        self.log_btn = ctk.CTkButton(self, text="Log Session", width=200, command=self._log_session)
        self.log_btn.pack(pady=10)

        # Stats
        self.stats_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13))
        self.stats_label.pack(pady=15)

    def _format_time(self, seconds: int) -> str:
        m, s = divmod(max(0, seconds), 60)
        return f"{m:02d}:{s:02d}"

    def _update_display(self, remaining: int):
        self.time_label.configure(text=self._format_time(remaining))

    def _start(self):
        try:
            mins = int(self.duration_var.get())
            if mins <= 0:
                raise ValueError
        except ValueError:
            mins = 25
            self.duration_var.set("25")

        if self.timer.remaining == self.timer.duration or self.timer.remaining <= 0:
            self.timer.reset(mins)

        self.timer.start()
        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal")
        self.duration_entry.configure(state="disabled")

    def _pause(self):
        self.timer.pause()
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled")

    def _reset(self):
        try:
            mins = int(self.duration_var.get())
        except ValueError:
            mins = 25
        self.timer.reset(mins)
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled")
        self.duration_entry.configure(state="normal")
        self._update_display(self.timer.remaining)

    def _on_timer_finish(self):
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled")
        self.duration_entry.configure(state="normal")
        self.time_label.configure(text="00:00")
        # You can add a sound here later

    def _log_session(self):
        # Calculate how much time was actually focused
        elapsed = (self.timer.duration - self.timer.remaining) / 60
        if elapsed < 0.5:  # ignore very short sessions
            return

        note = self.note_entry.get()
        self.logger.log_session(elapsed, note)
        self.note_entry.delete(0, "end")
        self._update_stats()

        # Optional: auto-reset after logging
        self._reset()

    def _update_stats(self):
        stats = self.logger.get_today_stats()
        self.stats_label.configure(
            text=f"Today: {stats['count']} sessions  •  {stats['total_minutes']} min focused"
        )