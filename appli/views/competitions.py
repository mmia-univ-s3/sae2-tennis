from flask import render_template

from appli.app import app


@app.route('/competitions/calendrier/')
def calendrier():
    return render_template('calendrier.html', title="Calendrier et résultats - Compétitions")


@app.route('/competitions/palmares/')
def palmares():
    return render_template('palmares.html', title="Palmarès - Competitions")


@app.route('/competitions/tournois/')
def tournois():
    return render_template('tournois.html', title="Tournois - Competitions")


@app.route('/competitions/tournois-internes/')
def internes():
    return render_template('internes.html', title="Tournois internes - Competitions")
