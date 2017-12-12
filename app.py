from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import PostForm

app = Flask(__name__)


app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from config import *
from util import *

db.create_all()
db.session.commit()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    flash("Post submitted")
    form = PostForm()
    if form.validate_on_submit():
        flash("Post submitted")
        post = Post(date    = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    author  = '',
                    subject = form.subject.data,
                    body    = form.body.data)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))
    posts = get_last_replies()
    return render_template('show_board.html', form=form, posts=posts[::-1])





#######################################


"""
@app.route('/add_reply', methods=['POST'])
def add_reply():
    #newPost = new_post()
    newPost = Posts(date    = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    author  = '',
                    subject = form.post.subject,
                    body    = form.post.data)
    db.session.add(newPost)
    db.session.commit()
    return redirect('/')
"""
if __name__ == '__main__':
    app.run(host="0.0.0.0")