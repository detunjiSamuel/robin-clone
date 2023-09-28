from flask import Blueprint, jsonify, request

from flask_login import current_user, login_user, logout_user, login_required


from .models import User, Asset, Transaction
from .forms import LoginForm, SignUpForm, AssetForm, TransactionForm
from db import db


def validation_errors_to_error_messages(validation_errors):
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


auth_routes = Blueprint('auth', __name__)
user_routes = Blueprint('users', __name__)



"""

AUTH ROUTES BEGIN HERE /api/auth

"""

@auth_routes.route('/')
def authenticate():

    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        response = user.json()
        response["assets"] = {asset.symbol: asset.json()
                              for asset in user.assets}

        totalStock = sum(
            [asset.quantity * asset.avg_price for asset in user.assets])
        response["totalStock"] = totalStock
        return jsonify(response)
    return {'errors': ['Unauthorized']}


@auth_routes.route('/login', methods=['POST'])
def login():

    form = LoginForm()

    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        user = User.query.filter(User.email == form.data['email']).first()
        login_user(user)

        response = user.json()
        response["assets"] = {asset.symbol: asset.json()
                              for asset in user.assets}

        totalStock = sum(
            [asset.quantity * asset.avg_price for asset in user.assets])

        response["totalStock"] = totalStock

        return jsonify(response)
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/logout')
def logout():

    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            first_name=form.data["first_name"],
            last_name=form.data["last_name"],
            email=form.data['email'],
            password=form.data['password'],
            networth=form.data["networth"],
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)

        response = user.json()
        response["assets"] = {asset.symbol: asset.json()
                              for asset in user.assets}

        totalStock = sum(
            [asset.quantity * asset.avg_price for asset in user.assets])

        response["totalStock"] = totalStock
        return response
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/unauthorized')
def unauthorized():
    return {'errors': ['Unauthorized']}, 401



"""

USER ROUTES BEGIN HERE /api/user

"""

@user_routes.route('/')
@login_required
def users():
    """
    GET ALL USERS
    """
    users = User.query.all()
    return {'users': [user.json() for user in users]}

@user_routes.route("/<email>")
def findEmail(email):
    """
    VERIFY USER EXISTS BY EMAIL
    """

    user = bool(User.query.filter(User.email.ilike(email)).all())
    if user:
        return jsonify(user), 409
    else:
        return jsonify(user), 200

@user_routes.route('/<int:id>')
@login_required
def user(id):
    """
    GET USER BY ID
    """

    user = User.query.get(id)
    return user.json()



@login_required
@user_routes.route('/upload', methods=['POST'])
def file_upload():
    """
    UPLOAD PROFILE PICTURE TO AWS S3
    
    """
    try:
        file = request.files['file']
        file_url = current_user.upload_profile(file)

        return {'file': file_url}

    except Exception as e:
        print(str(e))
        return {'error': 'Something went wrong'}, 500



@user_routes.route('/upload', methods=['DELETE'])
@login_required
def remove_profile():
    """
    DELETE PROFILE PICTURE FROM AWS S3
    """
    try:
        current_user.delete_profile()
        return {'message': 'Successfully removed'}
    except Exception as e:
        print(str(e))
        return {'error': 'Something went wrong'}, 500



@user_routes.route("/transaction", methods=["PUT"])
@login_required
def update_networth():
    """
    
    INITIATE TRANSACTION AND UPDATE USER NETWORTH
    
    """
    data = request.get_json()

    data["csrf_token"] = request.cookies['csrf_token']
    transactionForm = TransactionForm(**data)
    total_cost = data["price"] * data["quantity"]

    # MIN AMOUNT CHECK -> CANNOT SELL LESS THAN REQUIRED
    if not data["quantity"] > 0:
        return jsonify({"errors": {"amount": "Amount cannot be 0 "}}), 400

    if transactionForm.validate_on_submit():
        user = User.query.get(current_user.id)
        data["user_id"] = user.id
        transactionData = {**data}
        del transactionData["csrf_token"]
        del transactionData["name"]       
        # CHECK IF USER HAS ENOUGH FUNDS TO BUY
        if total_cost > user.networth and data["transaction_type"] == "buy":
            return jsonify({"errors": {"amount": "not enough funds."}}), 400

        # GET A USER's STOCK INFORMATION FOR A SUNGLE ASSET i.e how many shares of a stock(AAPLE) they own
        stock = Asset.query.filter(Asset.user_id == user.id).filter(
            Asset.symbol.ilike(data["symbol"])).one_or_none()


        if not stock and data["transaction_type"] == "buy":
            """
            HANDLES FIRST TIME BUYING THAT ASSET
												"""
            data["avg_price"] = data["price"]
            assetForm = AssetForm(**data)

            if assetForm.validate_on_submit():
                transction = Transaction(**transactionData)
                
                del data['csrf_token']
                del data["transaction_type"]
                del data["price"]
                stock = Asset(**data)
                
                user.networth = user.networth - total_cost
                db.session.add_all([transction, stock])
                db.session.commit()
                response = user.json()
                response["assets"] = {asset.symbol: asset.json()
                                      for asset in user.assets}

                totalStock = sum(
                    [asset.quantity * asset.avg_price for asset in user.assets])

                response["totalStock"] = totalStock
                return jsonify(response), 201

        if data["quantity"] > stock.quantity and data["transaction_type"] == "sell":
            """
            CANNOT SELL WHAT YOU DONT HAVE
												"""
            return jsonify({"errors": {"amount": "not enough stock"}}), 400

        if stock and data["transaction_type"] == "buy":
            final_quant = stock.quantity + data["quantity"]
            final_price = (stock.quantity * stock.avg_price) + \
                (data["price"] * data["quantity"])
            data["avg_price"] = final_price / final_quant
            data["quantity"] = data["quantity"] + stock.quantity
        elif stock and data["transaction_type"] == "sell":
            data["avg_price"] = stock.avg_price
            data["quantity"] = stock.quantity - data["quantity"]

        assetForm = AssetForm(**data)

        if assetForm.validate_on_submit():
            transction = Transaction(**transactionData)

            stock.quantity = data["quantity"]
            stock.avg_price = data["avg_price"]

            if data["transaction_type"] == "buy":
                user.networth = user.networth - total_cost
            else:
                user.networth = user.networth + total_cost

            if stock.quantity == 0:
                db.session.delete(stock)
                db.session.add(transction)
                db.session.commit()
                response = user.json()
                response["assets"] = {asset.symbol: asset.json()
                                      for asset in user.assets}

                totalStock = sum(
                    [asset.quantity * asset.avg_price for asset in user.assets])

                response["totalStock"] = totalStock
                return jsonify(response)

            db.session.add(transction)
            db.session.commit()
            response = user.json()
            response["assets"] = {asset.symbol: asset.json()
                                  for asset in user.assets}

            totalStock = sum(
                [asset.quantity * asset.avg_price for asset in user.assets])

            response["totalStock"] = totalStock
            return jsonify(response)

        else:
            return jsonify({"errors": assetForm.errors}), 400
    else:
        return {"errors": transactionForm.errors}, 400
