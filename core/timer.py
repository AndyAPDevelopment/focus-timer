import time
from threading import Thread

class FocusTimer:
    def __init__(self, duration_minutes: int = 25):
        self.duration = duration_minutes * 60  # seconds
        self.remaining = self.duration
        self.running = False
        self._thread = None
        self.on_tick = None      # callback(remaining_seconds)
        self.on_finish = None    # callback()

    def start(self):
        if self.running:
            return
        self.running = True
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def pause(self):
        self.running = False

    def reset(self, duration_minutes: int = None):
        self.running = False
        if duration_minutes is not None:
            self.duration = duration_minutes * 60
        self.remaining = self.duration
        if self.on_tick:
            self.on_tick(self.remaining)

    def _run(self):
        while self.running and self.remaining > 0:
            time.sleep(1)
            if self.running:
                self.remaining -= 1
                if self.on_tick:
                    self.on_tick(self.remaining)
        if self.remaining <= 0 and self.on_finish:
            self.on_finish()