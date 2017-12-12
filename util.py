from flask import request
from time import time
from models import Post
from app import db
from datetime import *

def get_last_replies():
    return db.session.query(Post).order_by(db.text('id desc'))#.limit(5)


def new_post():
    #post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)

    newPost = Post(date    = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    author  = '',
                    subject = form.post.subject,
                    body    = form.post.data)
    return newPost

