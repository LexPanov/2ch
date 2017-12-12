from flask import Flask, request, redirect, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.misaka import Misaka

app = Flask(__name__)
Misaka(app=app, escape    = True,
                no_images = True,
                wrap      = True,
                autolink  = True,
                no_intra_emphasis = True,
                space_headers     = True)

#from werkzeug.contrib.fixers import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from config import *
from util import *

db.create_all()
db.session.commit()

@app.route('/')
def show_board():
    list = get_last_replies()
    return render_template('show_board.html', entries=list[::-1])

@app.route('/add_reply', methods=['POST'])
def add_reply():
    newPost = new_post()
    db.session.add(newPost)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    #print(' * Running on http://127.0.0.1:5000/ (Press Ctrl-C to quit)')
    #print(' * Database is', SQLALCHEMY_DATABASE_URI)
    app.run(host="0.0.0.0")
