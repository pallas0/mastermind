from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2, requests
from sqlalchemy import desc
import threading
from time import sleep

from game import Game
from gametimer import GameTimer;
from models import db, BestScores

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route('/best_scores', methods=['GET'])
def best_scores():
    return jsonify({'best_scores': BestScores.get_all_scores()})

@app.route('/generate', methods=['GET'])
def generate_numbers():
    global game, game_timer
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
    print(game.number)
    game_timer = GameTimer(time=600, number=game.number, socket=socketio)

    timer_thread = threading.Thread(target=game_timer.run_timer)
    timer_thread.daemon = True
    timer_thread.start()

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
    data = request.json
    name = data['name']
    score = data['new_score']
    return jsonify(BestScores.update_best_score(name, score))


@socketio.on('time_up', namespace='/game')
def time_up():
   emit('time_up', {'number': game.number})


if __name__ == "__main__":
    app.run(debug=True)