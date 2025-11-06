from appli.app import app
from appli.statique import page_statique


@app.route('/formation/ecole-de-tennis/', methods=('GET', 'POST'))
def ecole():
    return page_statique("ecole", "ecole.html", "École de Tennis - Formation")
