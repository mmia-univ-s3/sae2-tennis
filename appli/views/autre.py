from appli.app import app, required_permission_lvl
from appli.statique import page_statique


@app.route('/autre-sports/', methods=('GET', 'POST'))
def autre():
    """Page statique 'Autres sports sur le stade'"""
    return page_statique("autre", "autre.html", "Autres sports sur le stade", "editeur")
