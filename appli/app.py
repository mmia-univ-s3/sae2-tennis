from flask import Flask
from flask_bootstrap5 import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy()
Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = "connexion"

db.init_app(app)
