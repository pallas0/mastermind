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
from models import db, BestScores, GameState

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
    global game_timer
    game = Game(number=[], guesses=[], feedback=[], player_won=[])
    game_state = GameState(state=game.to_dict())
    db.session.add(game_state)
    db.session.commit()
    game_timer = GameTimer(time=600, number=game.number, socket=socketio)

    timer_thread = threading.Thread(target=game_timer.run_timer)
    timer_thread.daemon = True
    timer_thread.start()

    return jsonify({'game_id': game_state.id, 'attempts': game.attempts})

@app.route('/compare_guess', methods=['POST'])
def compare_guess():
   game_id = request.json.get('gameID')
   game_state = GameState.query.get(game_id)
   if not game_state:
       return jsonify({'error': 'Game not found', 'status': 404})
   
   game = Game.from_dict(game_state.state)

   guess = request.json.get('guess')
   guess = [int(char) for char in guess]
   feedback = game.process_guess(guess)

   game_state.state = game.to_dict()
   db.session.commit()

   player_won = game.player_won
   number = []

   print(player_won)
   if player_won:
      print("hit")
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