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
    

    form = PostForm()
    if form.validate_on_submit():
        post = Post(date    = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    author  = '',
                    subject = form.subject.data,
                    body    = form.body.data)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))
    posts = get_last_replies()
    return render_template('show_board.html', form=form, posts=posts[::-1])

@app.route('/user/<nickname>')
#@login_required
def user(nickname):
    user = str(nickname)
    if user == "None":
        flash('User ' + "nickname" + ' not found.')
        return redirect(url_for('index'))


    return render_template('user.html',
        user = user)

@app.route('/delete/<id>')
def delete(id):
    delete_post(id)
    return redirect(url_for('index'))

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=4000)