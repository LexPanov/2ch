# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.
import os
from datetime import datetime
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, SQLAlchemyAdapter
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf_protect = CSRFProtect()

def create_app(extra_config_settings={}):
    app = Flask(__name__)
    app.config.from_object('app.settings')
    db.init_app(app) # Setup Flask-SQLAlchemy
    csrf_protect.init_app(app) # Setup WTForms CSRFProtect
    # Register blueprints
    from app.views.misc_views import main_blueprint
    app.register_blueprint(main_blueprint)
    #Setup login-pass validator
    from wtforms.validators import ValidationError

    def my_password_validator(form, field):
        password = field.data
        if len(password) < 3:
            raise ValidationError(_('Password must have at least 3 characters'))

    def my_username_validator(form, field):
        username = field.data
        if len(username) < 3:
            raise ValidationError(_('Username must be at least 3 characters long'))
        if not username.isalnum():
            raise ValidationError(_('Username may only contain letters and numbers'))

    # Setup Flask-User to handle user account related forms
    from .models.user_models import User, MyRegisterForm
    from .views.misc_views import user_profile_page

    db_adapter = SQLAlchemyAdapter(db, User)  # Setup the SQLAlchemy DB Adapter
    user_manager = UserManager(db_adapter, app,  # Init Flask-User and bind to app
                               register_form=MyRegisterForm,  # using a custom register form with UserProfile fields
                               user_profile_view_function=user_profile_page,
                               password_validator=my_password_validator,
                               username_validator=my_username_validator
                               )
    return app



