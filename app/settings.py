import os

APP_NAME = "2ch"

# Flask settings
DEBUG = True
CSRF_ENABLED = True
MAX_CONTENT_LENGTH = 20 * 1024 * 1024 #20Mb max upload
# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = False  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = False  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_ENABLE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = True  # Register and Login with username
USER_AFTER_LOGIN_ENDPOINT = 'main.home_page'
USER_AFTER_LOGOUT_ENDPOINT = 'main.home_page'
USER_SEND_PASSWORD_CHANGED_EMAIL = False
USER_SEND_REGISTERED_EMAIL = False
USER_SEND_USERNAME_CHANGED_EMAIL = False

# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#     python -c "import os; print repr(os.urandom(24));"
SECRET_KEY = 'This is an UNSECURE Secret. CHANGE THIS for production environments.'
