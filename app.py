from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from flask_login import LoginManager

from os import environ
from db import db

from apps.users.routes import user_routes , auth_routes
from apps.users.models import User

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'auth.unauthorized'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

# db = SQLAlchemy(app)


# db.create_all()

app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(auth_routes, url_prefix='/api/auth')

db.init_app(app)
Migrate(app, db)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"