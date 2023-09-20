from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from app import db


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

class WatchList_Stock(db.Model):
    __tablename__ = "watchlist_stocks"

    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey("watchlists.id"), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


    watchlist = db.relationship("WatchList", back_populates="watchlist_stocks")

    def json(self):
        return {
            'id': self.id,
            'watchlist_id': self.watchlist_id,
            'stock_symbol': self.stock_symbol
        }
    

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
            'watchlist_stocks': [stock.json() for stock in self.watchlist_stocks]
        }

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
    
class Transaction(db.Model):
    __tablename__ = 'transactions'


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    # sell or buy
    transaction_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    transaction_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates='transactions')
