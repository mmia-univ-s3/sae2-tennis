from functools import wraps
import os.path

from flask import Flask, render_template
from flask_bootstrap5 import Bootstrap
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy()
Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = "connexion"

if not os.path.exists("appli/static/upload"):
    os.mkdir("appli/static/upload")

db.init_app(app)

def get_nom_role(role):
    """
    Renvoie le nom d'affichage du rôle.

    Returns:
        Le nom d'affichage du rôle.
    """
    match role:
        case "administrateur":
            return "Administrateur·ice"
        case "publicateur":
            return "Publicateur·ice"
        case "editeur":
            return "Éditeur·ice"
        case "ecrivain":
            return "Écrivain·e"
        case _:
            return "???"

def get_role_permission_lvl(role):
    """
    Renvoie le niveau de permission (de 0 à 3) d'un rôle.

    Returns:
        Le niveau de permission du rôle.
    """
    match role:
        case "administrateur":
            return 3
        case "publicateur":
            return 2
        case "editeur":
            return 1
        case "ecrivain":
            return 0
        case _:
            return -1

def required_permission_lvl(role):
    """
    Un décorateur pour vérifier si l'utilisateur connecté a au moins le niveau de privilège requis.
    """
    def decorator(f):
        @login_required
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role_au_moins(role):
                return render_template("roles_required.html", title="Accès refusé",
                                       role=get_nom_role(role), get_nom_role=get_nom_role)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
