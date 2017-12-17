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
from hashlib import md5

MAX_IMAGE_SIZE = 1000, 1000
MAX_THUMB_SIZE = 220, 220
MAX_AVATAR_SIZE = 400, 400

main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/', methods = ['GET', 'POST'])
def home_page():
    form = PostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            author = current_user.username
            owner = current_user.id
            id = current_user.id
        else:
            author = "Аноним"
            owner = 0
            id = 0

        filename=''
        if form.file.data:
            data = form.file.data.read()
            hash = md5(data).hexdigest()
            filename = '{0}-{1}-{2}.jpg'.format(id,int(time.time()),hash)
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

@main_blueprint.route("/edit/<postid>", methods = ['GET', 'POST'])
def edit(postid):
    form = PostForm()
    post = db.session.query(Post).filter_by(id=postid).one()
    if current_user.is_authenticated:
        if post.owner==current_user.id:
            if form.validate_on_submit():
                if current_user.is_authenticated:
                    author = current_user.username
                    owner = current_user.id
                    id = current_user.id
                else:
                    author = "Аноним"
                    owner = 0
                    id = 0

                filename=''
                if form.file.data:
                    data = form.file.data.read()
                    hash = md5(data).hexdigest()
                    filename = '{0}-{1}-{2}.jpg'.format(id,int(time.time()),hash)
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

                post_mod = Post(id = postid,
                            date    = datetime.now().strftime("%d/%m/%y %a %H:%M:%S"),
                            author  = author,
                            subject = form.subject.data,
                            body    = form.body.data,
                            owner   = owner,
                            img     = filename
                            )

                if post.img:
                    filename = post.img
                    path = os.path.join("app/static/img", filename)
                    thumb_path = os.path.join("app/static/thumb", filename)
                    os.remove(path)
                    os.remove(thumb_path)

                db.session.delete(post)
                db.session.commit()
                db.session.add(post_mod)
                db.session.commit()
                return redirect(url_for('main.home_page'))
            return render_template("pages/edit.html", form=form, post=post)
    return redirect(url_for('main.home_page'))


@main_blueprint.route('/delete/<id>')
def delete(id):
    post = db.session.query(Post).filter_by(id=id).one()
    if current_user.is_authenticated:
        if post.owner==current_user.id or current_user.role==1:
            if post.img:
                filename = post.img
                path = os.path.join("app/static/img", filename)
                thumb_path = os.path.join("app/static/thumb", filename)
                os.remove(path)
                os.remove(thumb_path)
            db.session.delete(post)
        db.session.commit()
    return redirect(url_for('main.home_page'))


@main_blueprint.route('/pages/avatar', methods=['GET', 'POST'])
@login_required
def user_avatar_page():
    form = PostForm()
    if request.method == 'POST':

        filename=''
        if form.file.data:
            data = form.file.data.read()
            hash = md5(data).hexdigest()
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
    return render_template('pages/avatar.html', form=form)

@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    form = UserProfileForm(request.form)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        return redirect(url_for('main.home_page'))
    return render_template('pages/user_profile_page.html',  form=form)