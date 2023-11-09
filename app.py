from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import psycopg2, requests
from sqlalchemy import desc
import threading
from time import sleep

from game import Game
from gametimer import GameTimer;

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ameliarisner@localhost:5432/mastermind'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

class BestScores(db.Model):
    __tablename__ = 'BestScores'
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80))
    score = db.Column(db.Integer)


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
    global game, game_timer
    game = Game(number=[], guesses=[], feedback=[], player_won=[])
    game_timer = GameTimer(time=5, socket=socketio)

    timer_thread = threading.Thread(target=game_timer.run_timer)
    timer_thread.daemon = True
    timer_thread.start()

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
   #check if can just swap out line beneath w game.player_won
   player_won = game.player_won
   number = []

   if player_won:
      #if do not need to declare global time at top
      #maybe cut global game declaration
      game_timer.zero_time()
      number = game.number

   return jsonify({'feedback': feedback, 'player_won': player_won, 'number': number})

@app.route('/update_best_score', methods=['POST'])
def update_best_score():
   try:
      data = request.json
      name = data['name']
      score = data['new_score']

      ordered_scores = BestScores.query.order_by(desc(BestScores.score))
      highest_score_entry = ordered_scores.first()

      if highest_score_entry and ordered_scores.count() >= 3:
         db.session.delete(highest_score_entry)
         db.session.commit()
      
      new_score = BestScores(player_name=name, score=score)
      db.session.add(new_score)
      db.session.commit()

      return jsonify({'status': 200})
   
   except Exception as e:
      return jsonify({'error': str(e), 'status': 500})


@socketio.on('time_up', namespace='/game')
def time_up():
   emit('time_up')


if __name__ == "__main__":
    app.run(debug=True)