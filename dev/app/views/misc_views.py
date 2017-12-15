# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from datetime import datetime
from app import db
from app.models.user_models import UserProfileForm, Post, PostForm
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')



# The Home page is accessible to anyone
@main_blueprint.route('/', methods = ['GET', 'POST'])
def home_page():
    form = PostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            author = current_user.username
            owner = current_user.id
        else:
            author = "Аноним"
            owner = 0


        if form.file.data:
            print("OMG U COOL")
        post = Post(date    = datetime.now().strftime("%d/%m/%y %a %H:%M:%S"),
                    author  = author,
                    subject = form.subject.data,
                    body    = form.body.data,
                    owner   = owner
                    )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('main.home_page'))
    posts = db.session.query(Post).order_by(db.text('id desc'))
    return render_template('pages/home_page.html', form=form, posts=posts[::-1])
@main_blueprint.route('/delete/<id>')
def delete(id):
    post = db.session.query(Post).filter_by(id=id).one()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home_page'))

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('pages/user_page.html')

'''
# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
#@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')
'''

@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html', form=form)


