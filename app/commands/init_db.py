#import datetime
from flask import current_app
from flask_script import Command
from app import db
from app.models.user_models import User
from os import mkdir
from shutil import rmtree

class InitDbCommand(Command):
    """ Initialize the database."""
    def run(self):
        init_db()

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()
    try:  # Reset saved files on each start
        rmtree("app/static/img", True)
        rmtree("app/static/thumb", True)
        rmtree("app/static/avatar", True)
        mkdir("app/static/img")
        mkdir("app/static/thumb")
        mkdir("app/static/avatar")
    except OSError:
        pass

def create_users():
    db.create_all()
    user = create_user(u'admin1', 'a', 1)
    user = create_user(u'user1', 'a')
    user = create_user(u'admin2', 'a', 1)
    user = create_user(u'user2', 'a')
    db.session.commit()

def create_user(username, password, roleid = 0):
    """ Create new user """
    user = User(username=username,
                password=current_app.user_manager.hash_password(password),
                active=True,
                #confirmed_at=datetime.datetime.utcnow(),
                role=roleid)
    db.session.add(user)
    return user



