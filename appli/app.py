from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy()
Bootstrap(app)

db.init_app(app)
