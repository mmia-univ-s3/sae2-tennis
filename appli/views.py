from flask import render_template, redirect, url_for
from flask_login import logout_user

from .app import app

@app.route('/')
def index():
    return render_template('index.html', title="")

@app.route('/club/')
def club():
    return redirect(url_for('histoire'), 301)

@app.route('/club/histoire/')
def histoire():
    return render_template('histoire.html', title="Histoire et présentation - Club")

@app.route('/club/management/')
def management():
    return render_template('management.html', title="Management du club - Club")

@app.route('/club/articles/')
def articles():
    return render_template('articles.html', title="Articles du club - Club")

@app.route('/club/documents/')
def documents():
    return render_template('documents.html', title="Documents administratifs - Club")

@app.route('/competitions/')
def competitions():
    return redirect(url_for('calendrier'), 301)

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

@app.route('/formation/')
def formation():
    return redirect(url_for('tarifications'), 301)

@app.route('/formation/tarifications/')
def tarifications():
    return render_template('tarifications.html', title="Tarifications - Formation")

@app.route('/formation/ecole-de-tennis/')
def ecole():
    return render_template('ecole.html', title="École de Tennis - Formation")

@app.route('/partenaires/')
def partenaires():
    return render_template('partenaires.html', title="Partenaires")

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html', title="Contacts")

@app.route('/autre-sports/')
def autre():
    return render_template('autre.html', title="Autres sports sur le stade")

@app.route('/connexion/')
def connexion():
    return render_template('connexion.html', title="Se connecter")

@app.route('/deconnexion/')
def deconnexion():
    logout_user()
    return redirect(url_for("index"))

@app.errorhandler(404)
def e404(_):
    return render_template('error.html', error_code=404, error_message="La page est introuvable.")

@app.errorhandler(500)
def e500(_):
    return render_template('error.html', error_code=500, error_message="Une erreur s'est produite.")

@app.errorhandler(428)
def e428(_):
    return render_template('error.html', error_code=428, error_message="Cette méthode n'est pas autorisée.")

if __name__ == "__main__":
    app.run()
