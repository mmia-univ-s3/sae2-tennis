from appli.app import app
from appli.statique import page_statique


@app.route('/club/management/', methods=('GET', 'POST'))
def management():
    """Page statique 'Management du club'"""
    return page_statique("management", "management.html", "Management du club - Club", "editeur")
