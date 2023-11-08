from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import psycopg2, requests
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ameliarisner@localhost:5432/mastermind'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

class BestScores(db.Model):
    __tablename__ = 'BestScores'
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80))
    score = db.Column(db.Integer)



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
    

    """
    code scrap to add scores
    """
    #import pdb
    #pdb.set_trace()
    # score1 = BestScores(player_name='Rex', score=2)
    # score2 = BestScores(player_name='Amy', score=4)
    # score3 = BestScores(player_name='Jesus', score=5)
    # db.session.add(score1)
    # db.session.add(score2)
    # db.session.add(score3)
    # db.session.commit()
    # BestScores.query.delete()
    # db.session.commit()


@app.route('/best_scores', methods=['GET'])
def best_scores():
    best_scores = BestScores.query.order_by(BestScores.score).all()

    best_scores_list = [
        {
          'id': score.id,
          'player_name': score.player_name,
          'score': score.score
        }
        for score in best_scores
    ]
    return jsonify({'best_scores': best_scores_list})

@app.route('/generate', methods=['GET'])
def generate_numbers():
    global game
    game = Game(number=[], guesses=[], feedback=[], player_won=[])
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

    return jsonify({'attempts': game.attempts, 'number': game.number})

@app.route('/compare_guess', methods=['POST'])
def compare_guess():
   global game
   guess = request.json.get('guess')
   guess = [int(char) for char in guess]
   feedback = game.process_guess(guess)
   player_won = game.player_won
   return jsonify({'feedback': feedback, 'player_won': player_won})

@app.route('/update_best_score', methods=['POST'])
def update_best_score():
   try:
      data = request.json
      name = data['name']
      score = data['new_score']
      print("name: ", name)
      print("score: ", score)

      new_score = BestScores(player_name=name, score=score)
      db.session.add(new_score)
      db.session.commit()

      highest_score_entry = BestScores.query.order_by(desc(BestScores.score)).first()
      if highest_score_entry:
         db.session.delete(highest_score_entry)
         db.session.commit()

      return jsonify({'status': 200})
   
   except Exception as e:
      return jsonify({'error': str(e), 'status': 500})


if __name__ == "__main__":
    app.run(debug=True)