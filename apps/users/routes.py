from flask import Blueprint, jsonify, request

from flask_login import current_user, login_user, logout_user, login_required


from .models import User
from .forms import LoginForm, SignUpForm
from db import db


def validation_errors_to_error_messages(validation_errors):
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


auth_routes = Blueprint('auth', __name__)
user_routes = Blueprint('users', __name__)


@auth_routes.route('/')
def authenticate():

    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        response = user.to_dict()
        response["assets"] = {asset.symbol: asset.to_dict()
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

        response = user.to_dict()
        response["assets"] = {asset.symbol: asset.to_dict()
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
            username=form.data["username"]
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)

        response = user.to_dict()
        response["assets"] = {asset.symbol: asset.to_dict()
                              for asset in user.assets}

        totalStock = sum(
            [asset.quantity * asset.avg_price for asset in user.assets])

        response["totalStock"] = totalStock
        return response
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/unauthorized')
def unauthorized():
    return {'errors': ['Unauthorized']}, 401


@login_required
@user_routes.route('/upload', methods=['POST'])
def file_upload():
    try:
        file = request.files['file']
        file_url = current_user.upload_profile(file)

        return {'file': file_url}

    except Exception as e:
        print(str(e))
        return {'error': 'Something went wrong'}, 500


@login_required
@user_routes.route('/upload', methods=['DELETE'])
def remove_profile():
    try:
        current_user.delete_profile()
        return {'message': 'Successfully removed'}
    except Exception as e:
        print(str(e))
        return {'error': 'Something went wrong'}, 500


