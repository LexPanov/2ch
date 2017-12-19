# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, validators, FileField
from app import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    username = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    #confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'')
    role = db.Column(db.Integer(), nullable=False,server_default='0')
    avatar = db.Column(db.String)
    # Relationships
    #roles = db.relationship('Role', secondary='users_roles', backref=db.backref('users', lazy='dynamic'))


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    email = StringField('Email', validators=[validators.Email()])

# Define the User profile form
class UserProfileForm(FlaskForm):
    submit = SubmitField('Save')
    file = FileField('file', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])

class Post(db.Model):
    __tablename__ = 'posts'
    id        = db.Column(db.Integer, primary_key = True)
    owner     = db.Column(db.Integer, default = 0)
    date      = db.Column(db.String)
    author    = db.Column(db.String)
    subject   = db.Column(db.String)
    body      = db.Column(db.String)
    img       = db.Column(db.String)

class PostForm(FlaskForm):
    subject = StringField('subject', validators=[validators.Length(min=0, max=50)])
    body = TextAreaField('body', validators=[ validators.Length(min=0, max=1500)])
    file = FileField('file', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Send')