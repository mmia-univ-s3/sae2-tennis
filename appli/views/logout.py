from flask import redirect, url_for
from flask_login import logout_user

from appli.app import app


@app.route('/deconnexion/')
def deconnexion():
    logout_user()
    return redirect(url_for("index"))
