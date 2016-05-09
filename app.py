from flask import Flask, g
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.restless import APIManager

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = APIManager(app, flask_sqlalchemy_db=db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.before_request
def _before_request():
    g.user = current_user

bcrypt = Bcrypt(app)
