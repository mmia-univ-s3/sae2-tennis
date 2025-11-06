from appli.app import app
from appli.statique import page_statique


@app.route('/club/documents/', methods=('GET', 'POST'))
def documents():
    """Page statique 'Documents administratifs'"""
    return page_statique("documents", "documents.html", "Documents administratifs - Club")
