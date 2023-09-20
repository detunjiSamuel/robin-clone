from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from app import db



class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey(
                            'users.id'
                        ), nullable=False)
    title = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    ticker = db.Column(db.String)
    article_link = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates='news')

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "image": self.image,
            "ticker": self.ticker,
            "article_link": self.article_link,
        }
    

