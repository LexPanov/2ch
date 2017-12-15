# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from datetime import datetime
import os

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, SQLAlchemyAdapter
from flask_wtf.csrf import CSRFProtect

# Instantiate Flask extensions
db = SQLAlchemy()
csrf_protect = CSRFProtect()
#mail = Mail()
migrate = Migrate()


def create_app(extra_config_settings={}):
    """Create a Flask applicaction.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load App Config settings
    # Load common settings from 'app/settings.py' file
    app.config.from_object('app.settings')
    # Load local settings from 'app/local_settings.py'
    app.config.from_object('app.local_settings')
    # Load extra config settings from 'extra_config_settings' param
    app.config.update(extra_config_settings)

    # Setup Flask-Extensions -- do this _after_ app config has been loaded

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-Mail
    #mail.init_app(app)

    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)

    # Register blueprints
    from app.views.misc_views import main_blueprint
    app.register_blueprint(main_blueprint)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # Setup an error-logger to send emails to app.config.ADMINS
    #init_email_error_handler(app)

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



