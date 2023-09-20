from datetime import datetime

from app import db

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