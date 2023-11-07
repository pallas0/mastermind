from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

class Game:
  def __init__(self, number=[], guesses=[], feedback=[], player_won=[], number_length=4, attempts=10):
      self.number = number
      self.guesses = guesses
      self.feedback = feedback
      self.player_won = player_won
      self.number_length = number_length
      self.attempts = attempts

  def process_guess(self, guess):
    correct_numbers, correct_locations = 0,0
    number_dict = {}
    #make dict counting number of each number in the secret number
    for elem in self.number:
      number_dict[elem] = number_dict.get(elem,0) + 1
    #calculate correct_numbers and correct_locations
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
    print("feedback from process_guess: ", feedback)
    return feedback

  def update_history(self, guess, feedback):
    self.guesses.append(guess)
    self.feedback.append(feedback)
    self.attempts -= 1

  def check_gameover(self):
    if self.guesses[-1] == self.number :
      self.player_won.append(True)
    elif self.attempts == 0:
      self.player_won.append(False)
    


@app.route('/generate', methods=['GET'])
def genereate_numbers():
    global game
    game = Game()
    response = requests.get('https://www.random.org/integers', params={
        'num': game.number_length,
        'min': 0,
        'max': 7,
        'col': 1,
        'base': 10,
        'format': 'plain',
        'rnd': 'new'
    })
    game.number = [int(num) for num in response.text.split()]
    print(game.number)
    return jsonify({'attempts': game.attempts})

@app.route('/compare_guess', methods=['POST'])
def compare_guess():
   global game
   guess = request.json.get('guess')
   guess = [int(char) for char in guess]
   feedback = game.process_guess(guess)
   player_won = game.player_won
   return jsonify({'feedback': feedback, 'player_won': player_won})


if __name__ == "__main__":
    app.run(debug=True)