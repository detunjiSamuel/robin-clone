
from wtforms.validators import ValidationError


from .models import User


def user_exists_login(form, field):
    email = field.data
    user = User.query.filter(User.email == email).first()
    if not user:
        raise ValidationError('INVALID EMAIL PASED')


def password_matches_login(form, field):
    password = field.data
    email = form.data['email']
    user = User.query.filter(User.email == email).first()
    if not user:
        raise ValidationError('USER NOT EXISTS')
    if not user.check_password(password):
        raise ValidationError('WRONG CRED - PASSWORD')


def user_exists_signup(form, field):
    # Checking if user exists
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('EMAIL IN USE')