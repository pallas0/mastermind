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
from timer_manager import timer_manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route('/best_scores', methods=['GET'])
def best_scores():
    """
    This endpoint returns the best scores.
    """
    try:
        return jsonify({'best_scores': BestScores.get_all_scores()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['GET'])
def generate_numbers():
    """
    This endpoint generates numbers for the game, and starts the timer.
    """
    try:
      # create a game object 
      game = Game()
      game_state = GameState(state=game.to_dict())
      db.session.add(game_state)
      db.session.commit()

      # create a new timer associated with the game
      game_timer = timer_manager.create_timer(game_state.id, game.number, socketio, time=10)
      socketio.start_background_task(target=game_timer.run_timer)

      # return response
      return jsonify({'game_id': game_state.id, 'attempts': game.attempts})
    except Exception as e:
      return jsonify({'error': str(e)}), 500

@app.route('/compare_guess', methods=['POST'])
def compare_guess():
   """
    This endpoint compares the user's guess with the actual number.
    """
   try:
      game_id = request.json.get('gameID')
      game_state = GameState.query.get(game_id)
      if not game_state:
         return jsonify({'error': 'Game not found'}), 400
      
      game = Game.from_dict(game_state.state)

      guess = request.json.get('guess')
      guess = [int(char) for char in guess]
      feedback = game.process_guess(guess)

      game_state.state = game.to_dict()
      db.session.commit()

      player_won = game.player_won
      number = []

      game_timer = timer_manager.get_timer(game_id)
      if player_won:
         game_timer.zero_time()
         number = game.number

      return jsonify({'feedback': feedback, 'player_won': player_won, 'number': number})
   except Exception as e:
      return jsonify({'error': str(e)}), 500

@app.route('/update_best_score', methods=['POST'])
def update_best_score():
    """
    This endpoint updates the best score.
    """
    try:
      data = request.json
      name = data['name']
      score = data['new_score']
      return jsonify(BestScores.update_best_score(name, score))
    except Exception as e:
       return jsonify({'error': str(e)}), 500


@socketio.on('time_up', namespace='/game')
def time_up():
   """
    This function is triggered when the 'time_up' event is emitted.
    It emits a 'time_up' event to all connected clients.
    """
   emit('time_up')


if __name__ == "__main__":
    app.run(debug=True)