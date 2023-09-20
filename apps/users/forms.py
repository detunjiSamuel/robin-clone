from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange


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
