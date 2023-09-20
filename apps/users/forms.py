from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange , ValidationError


from .validators import user_exists_login, password_matches_login, user_exists_signup


class LoginForm(FlaskForm):
    email = StringField('email', validators=[
                        DataRequired(), user_exists_login])
    password = StringField('password', validators=[
                           DataRequired(), password_matches_login])


class SignUpForm(FlaskForm):
    first_name = StringField("First Name", [DataRequired()])
    last_name = StringField("Last Name", [DataRequired()])
    email = StringField('email', validators=[
                        DataRequired(), user_exists_signup])
    password = StringField('password', validators=[
                           DataRequired(), Length(min=10)])
    networth = FloatField(
        "Networth", [DataRequired(), NumberRange(max=10000000)])

class TransactionForm(FlaskForm):
    symbol = StringField("Symbol", [DataRequired()])
    transaction_type = StringField("Symbol", [DataRequired(message="Ammount cannot be 0")])
    price = FloatField("Price", [DataRequired()])
    quantity = FloatField("Quantity", [DataRequired()])

def checkZero():
    def _checkZero(form, field):
        if type(field.data) is float and field.data >= 0.00:
            return True
        else:
            raise ValidationError("Amount cannot be less than 0")
    return _checkZero


class AssetForm(FlaskForm):
    symbol = StringField("Symbol", [DataRequired()])
    name = StringField("Name", [DataRequired()])
    quantity = FloatField("Quantity", [checkZero()])
    avg_price = FloatField("Average Price", [DataRequired()])