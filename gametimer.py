from time import sleep


class GameTimer:

   
   def __init__(self, game_number, socket, time):
      """
        Initialize the GameTimer object.

        :param game_number: The number of the game.
        :param socket: The socket object to emit events.
        :param time: The time in seconds for the timer. Default is 600.
        """
      self.time = time
      self.game_number = game_number
      self.socket = socket

   def run_timer(self):
      """
      Run the timer. Decreases the time by 1 every second and emits a 'time_up' event when time is up.
      """
      try:
         while self.time > 0:
            sleep(1)
            self.time -= 1

            if self.time == 0:
               self.socket.emit('time_up', {'number': self.game_number}, namespace='/game')
               break
      except Exception as e:
         print(f"An error occurred while running the timer: {e}")
         return 500 
         
   def zero_time(self):
      """
      Set the time to zero.
      """
      self.time = 0