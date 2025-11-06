from appli.app import app
from appli.views.statique import page_statique


@app.route('/club/management/', methods=('GET', 'POST'))
def management():
    return page_statique("management", "management.html", "Management du club - Club")
