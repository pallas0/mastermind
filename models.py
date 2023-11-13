from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import requests
from typing import List, Optional, Tuple
import random
from flask import current_app

db = SQLAlchemy()

class Game(db.Model):
    DEFAULT_SECRET_CODE_LENGTH = 4
    DEFAULT_ATTEMPTS = 10

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each game
    secret_code = db.Column(db.String(DEFAULT_SECRET_CODE_LENGTH), nullable=False)  # The secret code that the player needs to guess
    guesses = db.Column(db.PickleType, default=[])  # List of guesses made by the player
    feedback = db.Column(db.PickleType, default=[])  # Feedback provided to the player for each guess
    player_won = db.Column(db.Boolean, default=False)  # Indicates whether the player has won the game
    secret_code_length = db.Column(db.Integer, default=DEFAULT_SECRET_CODE_LENGTH)  # The length of the secret code
    attempts = db.Column(db.Integer, default=10)  # The number of attempts the player has left
    game_over = db.Column(db.Boolean, default=False)  # Indicates whether the game is over

    def __init__(self, *args, **kwargs):
        if 'secret_code_length' not in kwargs:
            self.secret_code_length = self.DEFAULT_SECRET_CODE_LENGTH
        if 'attempts' not in kwargs:
            self.attempts = self.DEFAULT_ATTEMPTS
        super(Game, self).__init__(*args, **kwargs)
        self.secret_code = ''.join(str(num) for num in self.generate_secret_code())
        current_app.logger.debug(f"Initialized Game: {self}") 

    def __str__(self):
        """
        Create a string representation of the current state of the game.
        """
        return (f"Game ID: {self.id}, "
                f"Secret Code: {self.secret_code}, "
                f"Guesses: {self.guesses}, "
                f"Feedback: {self.feedback}, "
                f"Player Won: {self.player_won}, "
                f"Secret Code Length: {self.secret_code_length}, "
                f"Attempts Left: {self.attempts}, "
                f"Game Over: {self.game_over}")

    def generate_secret_code(self) -> List[int]:
      try:
        response = requests.get('https://www.random.org/integers', params={
          'num': self.secret_code_length,
          'min': 0,
          'max': 7,
          'col': 1,
          'base': 10,
          'format': 'plain',
          'rnd': 'new'
      })
        if response.status_code != 200:
          raise Exception(f"Secret generation: API request failed with status code {response.status_code}")
        if 'text/plain' not in response.headers.get('Content-Type', ''):
            raise Exception("Secret generation: API returns invalid response content type")
        return [int(num) for num in response.text.split()]
      except Exception as e:
        print(f"An error has occured: {e}")
        return [random.randint(0, 7) for _ in range(4)]

    def process_guess(self, guess: List[int]) -> str:
        """
        Processes a player's guess, updates the game state, and returns feedback.
        
        Args:
            guess (list): The player's guess.
        
        Returns:
            str: The feedback for the guess.
        """
        if not isinstance(guess, list) or not all(isinstance(i, int) for i in guess) or len(guess) != len(self.secret_code):
            raise ValueError("Guess must be a list of integers of the same length as the number.")
        correct_numbers, correct_locations = 0,0
        number_dict = {}
        
        secret_code_list = [int(digit) for digit in self.secret_code]

        for elem in secret_code_list :
            number_dict[elem] = number_dict.get(elem,0) + 1
        
        for i in range(len(secret_code_list)):
            if guess[i] == secret_code_list [i]:
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

    # potential bug here because we made player one a boolean instead of a 3 state thing
    def check_gameover(self):
        last_guess = [int(digit) for digit in self.secret_code]
        if self.guesses[-1] == last_guess:
            self.player_won = True
            self.game_over = True
        elif self.attempts == 0:
            self.game_over = True


class BestScores(db.Model):
    __tablename__ = 'BestScores'
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80))
    score = db.Column(db.Integer)
    game_id = db.Column(db.Integer)

    @classmethod
    def get_all_scores(cls):
        best_scores = cls.query.order_by(cls.score).all()
        best_scores_list = [
            {
                'id': score.id,
                'player_name': score.player_name,
                'score': score.score
            }
            for score in best_scores
        ]
        return best_scores_list
    
    @classmethod
    def update_best_score(cls, name, new_score, game_id):
        """
        This method updates the best score in the database.
        If there are already 3 scores, it deletes the highest score before adding the new one.
        It returns a dictionary with the status of the operation.
        """
        try:
            existing_entry = cls.query.filter_by(game_id=game_id).first()
            if existing_entry:
                return {'error': 'An entry with this game_id already exists', 'status': 400}
            
            ordered_scores = cls.query.order_by(desc(cls.score))
            highest_score_entry = ordered_scores.first()

            if highest_score_entry and ordered_scores.count() >= 3:
                db.session.delete(highest_score_entry)
                db.session.commit()
            
            # add the new score to the database
            new_score_obj= cls(player_name=name, score=new_score, game_id=game_id)
            db.session.add(new_score_obj)
            db.session.commit()

            return {'status': 200}
        
        except Exception as e:
            print(str(e))
            return {'error': str(e), 'status': 500}

# class GameState(db.Model):
#     __tablename__ = 'game_state'
#     id = db.Column(db.Integer, primary_key=True)
#     state = db.Column(db.PickleType)

