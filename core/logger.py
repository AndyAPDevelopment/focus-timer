import json
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "sessions.json"

class SessionLogger:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        if not DATA_FILE.exists():
            DATA_FILE.write_text("[]")

    def log_session(self, duration_minutes: float, note: str = ""):
        sessions = self._load()
        sessions.append({
            "date": str(date.today()),
            "duration_minutes": round(duration_minutes, 1),
            "note": note.strip()
        })
        self._save(sessions)

    def get_today_stats(self):
        sessions = self._load()
        today = str(date.today())
        today_sessions = [s for s in sessions if s["date"] == today]
        total_minutes = sum(s["duration_minutes"] for s in today_sessions)
        return {
            "count": len(today_sessions),
            "total_minutes": round(total_minutes, 1)
        }

    def _load(self):
        try:
            return json.loads(DATA_FILE.read_text())
        except Exception:
            return []

    def _save(self, data):
        DATA_FILE.write_text(json.dumps(data, indent=2))