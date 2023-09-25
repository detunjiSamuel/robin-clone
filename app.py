from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import generate_csrf
from flask_login import LoginManager

from os import environ
from db import db


from apps.users.routes import user_routes , auth_routes
from apps.stocks.routes import stock_routes , watchlist_routes , news_routes
from apps.users.models import User

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'auth.unauthorized'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

app.config['SECRET_KEY'] = environ.get('SECRET_KEY' , "test-secret")

# db = SQLAlchemy(app)


# db.create_all()

app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(stock_routes, url_prefix='/api/stock')
app.register_blueprint(watchlist_routes, url_prefix='/api/watchlists')
app.register_blueprint(news_routes, url_prefix='/api/news')

db.init_app(app)
Migrate(app, db)

CORS(app)

@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        # TODO CHANGE SECURE TO TRUE
        secure=False,
        #TODO CHNAGE SAMESITE TO 'Strict'
        samesite= None,
        httponly=True)
    return response

@app.route("/")
def hello_world():
    return "<p>CURRENTLY DOWN</p>"


