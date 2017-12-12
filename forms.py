from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    subject = StringField('subject', validators=[Length(min=0, max=50)])
    #name = StringField('name')
    body = TextAreaField('body', validators=[DataRequired(), Length(max=5)])
    #file = FileField('file', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
