from time import sleep


class GameTimer:
   def __init__(self, game_number, socket, time=600):
      self.time = time
      self.game_number = game_number
      self.socket = socket

   def run_timer(self):
      while self.time > 0:
         sleep(1)
         self.time -= 1


         if self.time == 0:
            self.socket.emit('time_up', {'number': self.game_number}, namespace='/game')
            break
         
   def zero_time(self):
      self.time = 0