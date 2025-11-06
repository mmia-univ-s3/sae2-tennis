from flask import redirect, url_for

from appli.app import app


@app.route('/club/')
def club():
    return redirect(url_for('histoire'), 301)


@app.route('/competitions/')
def competitions():
    return redirect(url_for('calendrier'), 301)


@app.route('/formation/')
def formation():
    return redirect(url_for('tarifications'), 301)
