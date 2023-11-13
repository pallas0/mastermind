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

from gametimer import GameTimer;
from models import db, Game, BestScores
from timer_manager import timer_manager

import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/generate', methods=['GET'])
def generate_numbers():
    """
    This endpoint generates numbers for the game, and starts the timer.
    
    Returns:
        JSON: A JSON object containing the game id and the number of attempts.
    """
    try:
      # create a game object 
      game = Game()
      db.session.add(game)
      db.session.commit()
      logger.debug(f"New Game DB Instance: {game}")

      # create a new timer associated with the game
      code = [int(digit) for digit in game.secret_code]
      game_timer = timer_manager.create_timer(game.id, code, socketio, time=600)
      socketio.start_background_task(target=game_timer.run_timer)

      # return response
      return jsonify({'game_id': game.id, 'attempts': game.attempts})
    except Exception as e:
      return jsonify({'error': str(e)}), 500

@app.route('/compare_guess', methods=['POST'])
def compare_guess():
   """
    This endpoint compares the user's guess with the actual number.
    
    Returns:
        JSON: A JSON object containing the feedback, whether the game is over,
        whether the player won, and the secret number if indeed game is over.
    """
   # try:
   data = request.json
   game_id = data.get('gameID')
   guess = [int(char) for char in data.get('guess')]

   game = Game.query.get(game_id)
   if not game:
      return jsonify({'error': 'Game not found'}), 400

   feedback = game.process_guess(guess)

   # zero the timer if the game is over
   game_timer = timer_manager.get_timer(game_id)
   if game.game_over and game_timer:
         game_timer.zero_time()
   
   # save the game to the db
   db.session.commit()

   return jsonify({
      'feedback': feedback,
      'game_over': game.game_over,
      'player_won': game.player_won,
      'number': game.secret_code if game.game_over else ""
   })
   # except ValueError as ve:
   #    return jsonify({'error': str(ve)}), 400
   # except Exception as e:
   #    return jsonify({'error': str(e)}), 500


@app.route('/best_scores', methods=['GET'])
def best_scores():
    """
    This endpoint returns the best scores.
    
    Returns:
        JSON: A JSON object containing the best scores.
    """
    try:
        return jsonify({'best_scores': BestScores.get_all_scores()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_best_score', methods=['POST'])
def update_best_score():
    """
    This endpoint updates the best score. It is currently only
    called by the frontend when the user has one of the top 3 scores
    (ie least number of attempts to win) ever recorded
    
    Returns:
        JSON: A JSON object containing the updated best score.
    """
    try:
      data = request.json
      name = data['name']
      score = data['new_score']
      game_id = data['gameID']
      return jsonify(BestScores.update_best_score(name, score, game_id))
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