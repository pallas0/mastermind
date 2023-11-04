from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

class Game:
  def __init__(self, number, guesses=[], feedback=[], player_won=[], number_length=4, attempts=10):
      self.number = number
      self.guesses = guesses
      self.feedback = feedback
      self.player_won = player_won
      self.number_length = number_length
      self.attempts = attempts

  def process_guess(self, guess):
    self.attempts -= 1
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
    #self.check_gameover()
    return feedback

  def update_history(self, guess, feedback):
    self.guesses.append(guess)
    self.feedback.append(feedback)

  #ok this flow we can iron out later
  # def check_gameover(self):
  #   if self.guesses[-1] == self.number :
  #     self.player_won.append(True)
  #     return True
  #   elif self.attempts == 0:
  #     self.player_won.append(False)
  #   return False
    

numbers = []
attempts = 10

@app.route('/generate', methods=['GET'])
def genereate_numbers():
    global numbers
    response = requests.get('https://www.random.org/integers', params={
        'num': 4,
        'min': 0,
        'max': 7,
        'col': 1,
        'base': 10,
        'format': 'plain',
        'rnd': 'new'
    })
    numbers = [int(num) for num in response.text.split()]
    attempts = 10
    return jsonify({'numbers': numbers, 'attempts': attempts})

@app.route('/guess', methods=['POST'])
def make_guess():
    global numbers
    guess = list(map(int, request.data.split()))
    return guess

if __name__ == "__main__":
    app.run(debug=True)