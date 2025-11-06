from flask import redirect, url_for

from appli.app import app


@app.route('/club/')
def club():
    """Redirection de 'club' vers la page d'histoire"""
    return redirect(url_for('histoire'), 301)


@app.route('/competitions/')
def competitions():
    """Redirection de 'competitions' vers la page de calendrier des compétitions"""
    return redirect(url_for('calendrier'), 301)


@app.route('/formation/')
def formation():
    """Redirection de 'formation' vers la page des tarifications"""
    return redirect(url_for('tarifications'), 301)
