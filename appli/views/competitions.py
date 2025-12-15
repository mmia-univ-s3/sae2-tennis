from flask import render_template, redirect, url_for
from flask_login import login_required
from sqlalchemy import or_

from appli.app import app, db
from appli.forms import FormInternes, FormConfirm
from appli.models import ChampionnatIndividuel, Joueur


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
    participant = ChampionnatIndividuel.query.filter(
        or_(ChampionnatIndividuel.categorie=="interne", ChampionnatIndividuel.categorie=="Interne"))
    resultat = []
    for match in participant:
        id_joueur = match.id
        joueur1 = match.joueur_1
        joueur2 = match.joueur_2
        score1 = match.score_1
        score2 = match.score_2
        resultat.append((id_joueur, joueur1, score1, joueur2, score2))
    return render_template('internes.html',
                           title="Tournois internes - Competitions", matchs=resultat)

@app.route('/competitions/tournois-internes/add/', methods=("GET", "POST"))
@login_required
def internes_add():
    form = FormInternes()
    joueurs = Joueur.query.all()
    choix = []
    for joueur in joueurs:
        choix.append((joueur.id, joueur.prenom + " " + joueur.nom))

    form.joueur1.choices =  choix
    form.joueur2.choices = choix

    if form.validate_on_submit():
        match = form.creation_interne()
        if match is not None:
            return redirect(url_for("internes"))
        return render_template("internes_add.html", title="Ajout d'un match",
                               form=form, error=True)
    return render_template("internes_add.html", title="Ajout d'un match",
                           form=form, error=False)

@app.route('/competitions/tournois-internes/<id_match>/update/', methods=("GET", "POST"))
@login_required
def internes_update(id_match):
    match = ChampionnatIndividuel.query.get(id_match)
    form = FormInternes(date=match.date_championnat, titre=match.titre, serie=match.serie,
                        categorie=match.categorie, niveau=match.niveau, joueur1=match.joueur_1,
                        joueur2=match.joueur_2, points1=match.score_1, points2=match.score_1)

    joueurs = Joueur.query.all()
    choix = []
    for joueur in joueurs:
        choix.append((joueur.id, joueur.prenom + " " + joueur.nom))

    form.joueur1.choices =  choix
    form.joueur2.choices = choix

    if form.validate_on_submit():
        match = form.creation_interne()
        if match is not None:
            return redirect(url_for("internes"))
        return render_template("internes_update.html",
                               title="Modification du match", form=form, error=True,
                               id_match=id_match)
    return render_template("internes_update.html", title="Modification du match",
                           form=form, error=False,id_match=id_match)

@app.route('/competitions/tournois-internes/<id_match>/delete/', methods=("GET", "POST"))
@login_required
def internes_delete(id_match):
    match = ChampionnatIndividuel.query.get(id_match)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(match)
        db.session.commit()
        return redirect(url_for('internes'))
    return render_template("internes_delete.html", title="Suppression du match",
                           form=form, id_match=id_match)
