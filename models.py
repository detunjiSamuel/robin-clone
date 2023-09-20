from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .app import app


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
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
            'joinedAt': self.created_at,
            'imageUrl': self.image_url
        }


class Asset(db.Model):
    __tablename__ = "assets"

    __table_args__ = (
        db.UniqueConstraint("user_id", "symbol"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)
    symbol = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    avg_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="assets")

    def json(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "quantity": self.quantity,
            "avgPrice": self.avg_price
        }



class StockSymbol(db.Model):
    __tablename__ = 'stock_symbols'
        
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)
    company = db.Column(db.String, nullable=False)


class WatchList(db.Model):
    __tablename__ = 'watchlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="watchlists")
    watchlist_stocks = db.relationship("WatchList_Stock",
                             back_populates="watchlist",
                             cascade="all, delete-orphan")

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'watchlist_stocks': [stock.to_dict() for stock in self.watchlist_stocks]
        }
