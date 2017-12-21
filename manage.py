"""This file sets up a command line manager.
Use "python manage.py" for a list of available commands.
Use "python manage.py runserver" to start the development web server on localhost:5000.
Use "python manage.py runserver --help" for additional runserver options.
"""

from flask_script import Manager

from app import create_app
from app.commands import InitDbCommand

# Setup Flask-Script with command line commands
manager = Manager(create_app)
manager.add_command('init_db', InitDbCommand)

if __name__ == "__main__":
    manager.run()
