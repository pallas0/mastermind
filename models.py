from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()

class BestScores(db.Model):
    __tablename__ = 'BestScores'
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80))
    score = db.Column(db.Integer)

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
    def update_best_score(cls, name, new_score):
        try:
            ordered_scores = cls.query.order_by(desc(cls.score))
            highest_score_entry = ordered_scores.first()

            if highest_score_entry and ordered_scores.count() >= 3:
                db.session.delete(highest_score_entry)
                db.session.commit()
            
            new_score = cls(player_name=name, score=new_score)
            db.session.add(new_score)
            db.session.commit()

            return {'status': 200}
        
        except Exception as e:
            return {'error': str(e), 'status': 500}
        
class GameState(db.Model):
    __tablename__ = 'game_state'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.PickleType)