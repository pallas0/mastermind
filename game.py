import requests

class Game:
  def __init__(self, number=[], guesses=[], feedback=[], player_won=[], number_length=4, attempts=10, game_over=False):
      """
      Initialize the Game class, generate and store the random number.
      
      Args:
          number (list): The number to guess.
          guesses (list): The list of guesses made.
          feedback (list): The list of feedback for each guess.
          player_won (list): The list of boolean values indicating if the player has won.
          number_length (int): The length of the number to guess.
          attempts (int): The number of attempts left.
          game_over (bool): Indicates if the game is over.
      """
      self.guesses = []
      self.feedback = feedback
      self.player_won = player_won
      self.number_length = number_length
      self.attempts = attempts
      self.game_over = game_over

      try:
        response = requests.get('https://www.random.org/integers', params={
          'num': self.number_length,
          'min': 0,
          'max': 7,
          'col': 1,
          'base': 10,
          'format': 'plain',
          'rnd': 'new'
      })
        if response.status_code != 200:
          raise Exception(f"Request failed with status code {response.status_code}")
        self.number = [int(num) for num in response.text.split()]
      except Exception as e:
        print(f"An error has occured: {e}")
        self.number = []
      
  
  def to_dict(self):
    """
    Converts the current game state to a dictionary.
    
    Returns:
        dict: The current game state.
    """
    return {
      'number': self.number,
      'guesses': self.guesses,
      'feedback': self.feedback,
      'player_won': self.player_won,
      'number_length': self.number_length,
      'attempts': self.attempts,
      'game_over': self.game_over
    }
  
  @staticmethod
  def from_dict(data):
    """
    Creates a new game instance from a dictionary.
    
    Args:
        data (dict): The game state.
    
    Returns:
        Game: The game instance.
    """
    game = Game()
    game.number = data['number']
    game.guesses = data['guesses']
    game.feedback = data['feedback']
    game.player_won = data['player_won']
    game.number_length = data['number_length']
    game.attempts = data['attempts']
    game.game_over = data['game_over']
    return game
  

  def process_guess(self, guess):
    """
    Processes a player's guess, updates the game state, and returns feedback.
    
    Args:
        guess (list): The player's guess.
    
    Returns:
        str: The feedback for the guess.
    """
    if not isinstance(guess, list) or not all(isinstance(i, int) for i in guess) or len(guess) != len(self.number):
      raise ValueError("Guess must be a list of integers of the same length as the number.")
    correct_numbers, correct_locations = 0,0
    number_dict = {}
    
    for elem in self.number:
      number_dict[elem] = number_dict.get(elem,0) + 1
    
    for i in range(len(self.number)):
      if guess[i] == self.number[i]:
        correct_locations += 1
      if guess[i] in number_dict:
        number_dict[guess[i]] -= 1
        if number_dict[guess[i]] == 0:
          number_dict.pop(guess[i])
        correct_numbers += 1

    feedback = f"{correct_numbers} right numbers, {correct_locations} in the right location"
    self.update_history(guess, feedback)
    self.check_gameover()
    return feedback

  def update_history(self, guess, feedback):
    """
    Updates the game history with the latest guess and feedback.
    """
    self.guesses.append(guess)
    self.feedback.append(feedback)
    self.attempts -= 1

  def check_gameover(self):
    """
    Checks if the game is over based on the latest guess or remaining attempts.
    """
    if self.guesses[-1] == self.number :
      self.player_won.append(True)
      self.game_over = True
    elif self.attempts == 0:
      self.player_won.append(False)
      self.game_over = True