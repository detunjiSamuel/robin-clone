from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import StringField, BooleanField, IntegerField

class WatchListForm(FlaskForm): 
    name = StringField('List Name', validators=[DataRequired('Please input name.')])

class AddStockForm(FlaskForm):
    symbol = StringField('symbol', validators=[DataRequired()])

class AddArticleForm(FlaskForm):
    like = BooleanField('Like', default=True)
    user_id = IntegerField(
        "User ID", [DataRequired(message="User id required")])
    title = StringField("Title", [DataRequired(message="Title required")])
    source = StringField("Source", [DataRequired(message="Source required")])
    image = StringField("Image", [DataRequired(message="Image Link required")])
    article_link = StringField(
        "Article Link", [DataRequired(message="Article Link required")])