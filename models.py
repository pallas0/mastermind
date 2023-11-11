from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()

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
        
class GameState(db.Model):
    __tablename__ = 'game_state'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.PickleType)

