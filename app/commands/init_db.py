# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User#, Role
import os 
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
        os.mkdir("app/static/img")
        os.mkdir("app/static/thumb")
        os.mkdir("app/static/avatar")
    except OSError:
        pass

def create_users():

    # Create all tables
    db.create_all()

    # Add users
    user = find_or_create_user(u'admin1', 'a', 1)
    user = find_or_create_user(u'user1', 'a')
    user = find_or_create_user(u'admin2', 'a', 1)
    user = find_or_create_user(u'user2', 'a')

    # Save to DB
    db.session.commit()

def find_or_create_user(username, password, roleid = 0):
    """ Find existing user or create new user """
    user = User.query.filter(User.username == username).first()
    if not user:
        user = User(username=username,
                    password=current_app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.datetime.utcnow(),
                    role=roleid)

        db.session.add(user)
    return user



