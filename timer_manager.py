# timer_manager.py
import threading
from gametimer import GameTimer

class TimerManager:

    DEFAULT_TIME_LENGTH = 600
    def __init__(self):
        self.timers = {}
        self.lock = threading.Lock()

    def create_timer(self, game_id, game_number, socket, time=DEFAULT_TIME_LENGTH):
        with self.lock:
            if game_id not in self.timers:
                self.timers[game_id] = GameTimer(game_number, socket, time)
                return self.timers[game_id]

    def get_timer(self, game_id):
        with self.lock:
            return self.timers.get(game_id)

    def remove_timer(self, game_id):
        with self.lock:
            if game_id in self.timers:
                del self.timers[game_id]

timer_manager = TimerManager()
