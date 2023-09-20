from flask import Flask, request, jsonify, make_response

from os import environ



app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')






# db.create_all()



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"