from flask import Blueprint, request, jsonify
from sqlalchemy import case
from flask_login import login_required, current_user
import requests
import os

from .models import StockSymbol , WatchList , WatchList_Stock , News
from .forms import WatchListForm , AddStockForm , AddArticleForm

from db import db

stock_routes = Blueprint('stock', __name__)
watchlist_routes =  Blueprint('watchlists', __name__)
news_routes = Blueprint('news', __name__)


"""
STOCK ROUTES BEGIN HERE /api/stock

USE :  ENDPOINTS ALL FOR GETTING INFORMATION ABOUT STOCKS

"""

@stock_routes.route('/get-key')
def get_key():
    apikey = os.environ.get('STOCK_API_KEY')
    return {'api_key': apikey}

@stock_routes.route('/get-data/<string:symbol>')
def get_data(symbol):
    func = request.args.get('func') or 'daily'
    apikey = os.environ.get('STOCK_API_KEY')
    url = f'https://www.alphavantage.co/query?function={"TIME_SERIES_DAILY_ADJUSTED" if func == "daily" else "TIME_SERIES_INTRADAY"}&symbol={symbol}&apikey={apikey}&outputsize=full{"&interval=5min" if func == "minutely" else ""}'

    res = requests.get(url).json()
    return res


@stock_routes.route('/search/<string:keyword>')
def search_symbols(keyword):
    result = [
        {'symbol': item.stock_symbol, 'name': item.company} 
        for item in StockSymbol.query.filter(StockSymbol.stock_symbol.ilike(f'%{keyword}%') 
                                             | 
                                             StockSymbol.company.ilike(
        f'%{keyword}%')).order_by(case((StockSymbol.stock_symbol.startswith(keyword), 0), (StockSymbol.company.startswith(keyword), 1), else_=2)).limit(7)]

    return jsonify(result)


@stock_routes.route("/company-information/<string:ticker>")
def company_information(ticker):
    apikey = os.environ.get('STOCK_API_KEY')
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={apikey}"
    data = requests.get(url).json()

    if "Address" in data:
        company_info = {
            "about": {
                "Address": data["Address"],
                "Description": data["Description"],
                "Industry": data["Industry"],
                "Exchange": data["Exchange"],
                "Name": data["Name"]
            },
            "statistics": {
                "PERatio": data["PERatio"],
                "MarketCap": data["MarketCapitalization"],
                "DividendYield": data["DividendYield"],
                "YearHigh": data["52WeekHigh"],
                "YearLow": data["52WeekLow"],
                "AnalystTargetPrice": data["AnalystTargetPrice"],
                "Sector": data["Sector"],
                "Symbol": data["Symbol"]
            }
        }

        return jsonify(company_info)
    else:
        return jsonify({"errors": "Data not available at the moment"}), 417

"""
WATCHLIST ROUTES BEGIN HERE /api/watchlists

"""


@watchlist_routes.route('/', methods=['POST'])
@login_required
def create_watchlist():
    current_user_info = current_user.json()
    current_user_id = current_user_info['id']
    form = WatchListForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate():
        try:
            new_watchlist = WatchList(
                name = form.data['name'],
                user_id = current_user_id
            )
            db.session.add(new_watchlist)
            db.session.commit()
            return new_watchlist.json(), 201
        except Exception:
            return {'error': 'there is an error in form.validate()'}
    if form.errors:
        return {'error': form.errors}


@watchlist_routes.route('/<int:watchlist_id>', methods=['PUT'])
@login_required
def update_watchlist(watchlist_id):
    current_user_info = current_user.json()
    current_user_id = current_user_info['id']
    update_watchlist = WatchList.query.get(watchlist_id)
    if update_watchlist:
        if update_watchlist.user_id == current_user_id:
            data = request.get_json()
            update_watchlist.name = data['name']
            db.session.commit()
            return update_watchlist.json(), 200
        else:
            return {'error': {
                'message': 'Forbidden',
                'statusCode': 403
            }}, 403
    else:
        return {'error': {
            'message': 'Can not find watchlist',
            'statusCode': 404
        }}, 404

#add stock to watchlist
@watchlist_routes.route('/<int:watchlist_id>/stocks', methods=['POST'])
@login_required
def add_stock(watchlist_id):
    current_user_info = current_user.json()
    current_user_id = current_user_info['id']
    watchlist = WatchList.query.get(watchlist_id)
    if not watchlist:
        return {'error': {
            'message': 'Can not find watchlist',
            'statusCode': 404
        }}
    if watchlist.user_id != current_user_id:
        return {'error': {
                'message': 'Forbidden',
                'statusCode': 403
            }}
    form = AddStockForm()
    form['csrf_token'].data = request.cookies['csrf_token']


    if form.validate():
        symbol = form.data['symbol']
        if symbol in [w.stock_symbol for w in watchlist.watchlist_stocks]:
            return {
                'error': {
                    'message': 'Stock already exist',
                    'statusCode': 403
                }
            }, 403
        try:
            new_stock = WatchList_Stock(
                watchlist_id = watchlist_id,
                stock_symbol = form.data['symbol']
            )
            db.session.add(new_stock)
            db.session.commit()
            return new_stock.json(), 200
        except Exception:
            return {'error': 'there is an error in form.validate()'}
    if form.errors:
        return {'error': form.errors}

@watchlist_routes.route('/current')
@login_required
def user_watchlists():
    current_user_info = current_user.json()
    current_user_id = current_user_info['id']
    user_watchlists = WatchList.query.filter(WatchList.user_id == current_user_id ).all()
    return {'watchlists': [watchlist.json() for watchlist in user_watchlists]}

#remove stock to watchlist
@watchlist_routes.route('/stocks/<int:stock_id>', methods=['DELETE'])
@login_required
def delete_stock(stock_id):
    current_user_info = current_user.json()
    current_user_id = current_user_info['id']
    delete_stock = WatchList_Stock.query.get(stock_id)
    if not delete_stock:
        return {'error': {
            'message': 'Can not find watchlist',
            'statusCode': 404
        }}, 404
    watchlist = WatchList.query.get(delete_stock.watchlist_id)
    if watchlist.user_id != current_user_id:
        return {'error': {
                'message': 'Forbidden',
                'statusCode': 403
        }}, 403
    db.session.delete(delete_stock)
    db.session.commit()
    return {'message': 'Successfully delete stock'}

@watchlist_routes.route('/')
@login_required
def all_watchlists():
    """
    Query for all watchlists and returns them in a list of watchlist dictionaries
    """
    watchlists = WatchList.query.all()
    return {'watchlists': [watchlist.json() for watchlist in watchlists]}


#delete watchlist
@watchlist_routes.route('/<int:watchlist_id>', methods=['DELETE'])
@login_required
def delete_watchlist(watchlist_id):
    current_user_info = current_user.json()
    current_user_id = current_user_info['id']
    delete_watchlist = WatchList.query.get(watchlist_id)
    if delete_watchlist:
        if delete_watchlist.user_id == current_user_id:
            db.session.delete(delete_watchlist)
            db.session.commit()
            return {'message': 'Successfully delete'}
        else:
            return {'error': {
                'message': 'Forbidden',
                'statusCode': 403
            }}, 403
    else:
        return {'error': {
            'message': 'Can not find watchlist',
            'statusCode': 404
        }}, 404



"""
NEWS ROUTES BEGIN HERE /api/news

"""

@news_routes.route("/")
def get_all_news():
    key_choice = os.getenv("STOCK_API_KEY")
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={key_choice}&sort=LATEST'
    r = requests.get(url)
    data = r.json()
    if "feed" in data:
        feed = data["feed"]
        article_data = [{"source": article["source"], "title": article["title"],
                        "image": article["banner_image"], "url": article["url"],
                         "tickers": [stock["ticker"] for stock in article["ticker_sentiment"]]} for article in feed if "banner_image" in article and article["banner_image"]]

        return jsonify(article_data[:25])
    else:
        return jsonify({"error": "No news found at the moment"}), 500
 

@news_routes.route("/<string:ticker>")
def get_news_by_ticker(ticker):
    # return a an enumarated list of keys
    news_api_keys = os.getenv("STOCK_API_KEY")

    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={news_api_keys}&tickers={ticker}&sort=LATEST'
    r = requests.get(url)
    data = r.json()

    if "feed" in data:
        feed = data["feed"]
        article_data = [{"source": article["source"], "title": article["title"],
                         "image": article["banner_image"], "url": article["url"],
                         "tickers": [stock["ticker"] for stock in article["ticker_sentiment"]]} for article in feed if "banner_image" in article and article["banner_image"]]
        return jsonify(article_data[:5])
    else:
        return jsonify({"error": "No news found at the moment"}), 500

@news_routes.route("/liked", methods=["POST"])
@login_required
def add_article_like():
    add_article_form = AddArticleForm()
    add_article_form['csrf_token'].data = request.cookies['csrf_token']

    current_user_info = current_user.json()
    current_user_id = current_user_info['id']
    # sending to the database

    if add_article_form.validate_on_submit():
        new_liked_article = News(
            like=True,
            user_id=current_user_id,
            title=add_article_form.data['title'],
            source=add_article_form.data['source'],
            image=add_article_form.data['image'],
            article_link=add_article_form.data['article_link']
        )
        db.session.add(new_liked_article)
        db.session.commit()
        return jsonify(new_liked_article.json())
    else:
        return jsonify(add_article_form.errors), 406

@news_routes.route("/liked", methods=["GET"])
@login_required
def get_article_like():
    liked = News.query.filter(News.like == '1').filter(
        News.user_id == current_user.id).all()
    return jsonify([news.json() for news in liked]), 200


@news_routes.route("/liked/<int:news_id>", methods=["DELETE"])
@login_required
def delete_article_like(news_id):
    # find the liked article where user id is the same as the user_id
    # delete
    article = News.query.get(news_id)
    if current_user.id != article.user_id:
        return {
            "message": "This like does not belong to you"
        }

    db.session.delete(article)
    db.session.commit()
    return {"message": "Deleted like"}
