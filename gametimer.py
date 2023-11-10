from time import sleep

class GameTimer:
   def __init__(self, time=600, number=[], socket=[]):
      self.time = time
      self.number = number
      self.socket = socket

   def run_timer(self):
      while self.time > 0:
         sleep(1)
         self.time -= 1

         if self.time == 0 and self.socket:
            self.socket.emit('time_up', {'number': self.number}, namespace='/game')
            break
         
   def zero_time(self):
      self.time = 0