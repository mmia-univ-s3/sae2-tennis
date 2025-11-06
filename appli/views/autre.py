from appli.app import app
from appli.views.statique import page_statique


@app.route('/autre-sports/', methods=('GET', 'POST'))
def autre():
    return page_statique("autre", "autre.html", "Autres sports sur le stade")
