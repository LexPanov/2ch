from flask import request
from time import time
from models import Posts
from app import db
from datetime import *

def get_last_replies():
    return db.session.query(Posts).order_by(db.text('id desc'))#.limit(5)


def new_post():
    newPost = Posts(name    = '',
                    subject = request.form['subject'],
                    text    = request.form['comment'],
                    date    = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return newPost



