# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from datetime import datetime
from app import db
from app.models.user_models import UserProfileForm, Post, PostForm, User
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


import os
from PIL import Image, ImageFile
import time
from hashlib import blake2s

MAX_IMAGE_SIZE = 1000, 1000
MAX_THUMB_SIZE = 220, 220
MAX_AVATAR_SIZE = 400, 400
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

        filename=''
        print(form.file.data)
        if form.file.data:
            data = form.file.data.read()
            hash = blake2s(data, digest_size=16).hexdigest()
            filename = '{0}-{1}-{2}.jpg'.format(current_user.id,int(time.time()),hash)
            path = os.path.join("app/static/img", filename)
            thumb_path = os.path.join("app/static/thumb", filename)
            image_parser = ImageFile.Parser()
            try:
                image_parser.feed(data)
                image = image_parser.close()
            except IOError:
                filename = ''
                raise
            thumb = image.copy()
            image.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
            thumb.thumbnail(MAX_THUMB_SIZE, Image.ANTIALIAS)
            if image.mode != 'RGB':
                image = image.convert('RGB')
                thumb = thumb.convert('RGB')
            image.save(path)
            thumb.save(thumb_path)


        post = Post(date    = datetime.now().strftime("%d/%m/%y %a %H:%M:%S"),
                    author  = author,
                    subject = form.subject.data,
                    body    = form.body.data,
                    owner   = owner,
                    img     = filename
                    )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('main.home_page'))
    posts = db.session.query(Post).order_by(db.text('id desc'))
    return render_template('pages/home_page.html', form=form, posts=posts[::-1])
@main_blueprint.route('/delete/<id>')
def delete(id):
    post = db.session.query(Post).filter_by(id=id).one()
    filename = post.img
    path = os.path.join("app/static/img", filename)
    thumb_path = os.path.join("app/static/thumb", filename)
    os.remove(path)
    os.remove(thumb_path)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home_page'))

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('pages/user_page.html')

@main_blueprint.route('/pages/avatar', methods=['GET', 'POST'])
@login_required
def user_avatar_page():
    # Initialize form
    form = PostForm()
    if request.method == 'POST':
        filename=''
        print(form.file.data)
        if form.file.data:
            data = form.file.data.read()
            hash = blake2s(data, digest_size=16).hexdigest()
            filename = '{0}-{1}-{2}.jpg'.format(current_user.id,int(time.time()),hash)
            path = os.path.join("app/static/avatar", filename)

            image_parser = ImageFile.Parser()
            try:
                image_parser.feed(data)
                image = image_parser.close()
            except IOError:
                filename = ''
                raise
            thumb = image.copy()
            image.thumbnail(MAX_AVATAR_SIZE, Image.ANTIALIAS)

            if image.mode != 'RGB':
                image = image.convert('RGB')

            

            if current_user.avatar:
                name = current_user.avatar
                pat = os.path.join("app/static/avatar", name)
                os.remove(pat)

            image.save(path)
            current_user.avatar = filename
            db.session.commit()

    # Process GET or invalid POST
    return render_template('pages/avatar.html', form=form)




@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form)

    # Process valid POST

    if form.validate_on_submit():


        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',  form=form)


