from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    nick_name = db.Column(db.String, nullable=False, default=nick_name_default)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    networth = db.Column(db.Float, default=0.00)
    image_url = db.Column(db.String, nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            "networth": self.networth,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'nickname': self.nick_name,
            'joinedAt': self.created_at,
            'imageUrl': self.image_url
        }

# db.create_all()



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"