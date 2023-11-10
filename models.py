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