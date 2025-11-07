from flask import render_template, redirect, url_for
from flask_login import login_required

from appli.app import app, db
from appli.models import ChampionnatIndividuel, ChampionnatEquipe, Affronter, Joueur, Classer
from appli.forms import FormChampionnatEquipe, FormChampionnatIndividuel, FormClasser


@app.route('/competitions/calendrier/')
def calendrier():
    """Permet d'afficher la page concernant le calendrier des tournois"""
    list_comp_indiv = ChampionnatIndividuel.query.order_by(\
        ChampionnatIndividuel.date_championnat.desc()).all()
    list_comp_equipe = ChampionnatEquipe.query.order_by(\
        ChampionnatEquipe.date_championnat.desc()).all()
    return render_template('calendrier.html', title="Calendrier - Compétitions",
                           comp_indiv=list_comp_indiv, comp_equipe=list_comp_equipe)


@app.route('/competitions/tournoi/<type_tournoi>/<int:id_championnat>/delete/',
           methods=('GET', 'POST'))
@login_required
def tournoi_delete(type_tournoi: str, id_championnat: int):
    """Permet de supprimer un tournoi de la base de données

    Args:
        type_tournoi (str): Indique si le tournoi est "individuel" ou en "equipe"
        id_championnat (int): L'identifiant du tournoi dans la base de données
    """
    if type_tournoi == "individuel":
        championnat = ChampionnatIndividuel.query.get(id_championnat)
        form = FormChampionnatIndividuel(titre=championnat.titre,
                                         date_championnat=championnat.date_championnat,
                                         categorie=championnat.categorie, serie=championnat.serie,
                                         niveau=championnat.niveau)
    else:
        championnat = ChampionnatEquipe.query.get(id_championnat)
        form = FormChampionnatEquipe(titre=championnat.titre,
                                     date_championnat=championnat.date_championnat,
                                     categorie=championnat.categorie, serie=championnat.serie)
    if form.validate_on_submit():
        db.session.delete(championnat)
        db.session.commit()
        return redirect(url_for("calendrier"))
    return render_template('tournoi_delete.html', title="Supprimer un tournoi", form=form,
                           type_tournoi=type_tournoi, championnat=championnat)


@app.route('/competitions/tournoi/<type_tournoi>/<int:id_championnat>/update/',
           methods=('GET', 'POST'))
@login_required
def tournoi_update(type_tournoi: str, id_championnat: int):
    """Permet de modifier un tournoi de la base de données

    Args:
        type_tournoi (str): Indique si le tournoi est "individuel" ou en "equipe"
        id_championnat (int): L'identifiant du tournoi dans la base de données
    """
    if type_tournoi == "individuel":
        championnat = ChampionnatIndividuel.query.get(id_championnat)
        form = FormChampionnatIndividuel(titre=championnat.titre,
                                         date_championnat=championnat.date_championnat,
                                         categorie=championnat.categorie, serie=championnat.serie,
                                         niveau=championnat.niveau)
    else:
        championnat = ChampionnatEquipe.query.get(id_championnat)
        form = FormChampionnatEquipe(titre=championnat.titre,
                                     date_championnat=championnat.date_championnat,
                                     categorie=championnat.categorie, serie=championnat.serie)
    if form.validate_on_submit():
        championnat.titre = form.titre.data
        championnat.date_championnat = form.date_championnat.data
        championnat.categorie = form.categorie.data
        championnat.serie = form.serie.data
        if type_tournoi == "individuel":
            championnat.niveau = form.niveau.data
        db.session.commit()
        return redirect(url_for("calendrier"))
    return render_template('tournoi_update.html', title="Modifier un tournoi", form=form,
                           type_tournoi=type_tournoi, championnat=championnat)


@app.route('/competitions/tournoi/<type_tournoi>/add', methods=('GET', 'POST'))
@login_required
def tournoi_add(type_tournoi: str):
    """Permet d'ajouter un tournoi dans la base de données

    Args:
        type_tournoi (str): Indique si le tournoi est "individuel" ou en "equipe"
    """
    if type_tournoi == "individuel":
        form = FormChampionnatIndividuel()
        championnat = ChampionnatIndividuel(titre=form.titre.data,
                                            date_championnat=form.date_championnat.data,
                                            categorie=form.categorie.data, serie=form.serie.data,
                                            niveau=form.niveau.data)
    else:
        form = FormChampionnatEquipe()
        championnat = ChampionnatEquipe(titre=form.titre.data,
                                        date_championnat=form.date_championnat.data,
                                        categorie=form.categorie.data, serie=form.serie.data)
    if form.validate_on_submit():
        db.session.add(championnat)
        db.session.commit()
        return redirect(url_for("calendrier"))
    return render_template('tournoi_add.html', title="Ajouter un tournoi", form=form,
                           type_tournoi=type_tournoi, championnat=championnat)


@app.route('/competitions/palmares/')
def palmares():
    return render_template('palmares.html', title="Palmarès - Competitions")


@app.route('/competitions/tournoi/<type_tournoi>/<int:id_championnat>/')
def tournoi(type_tournoi: str, id_championnat: int):
    """Permet d'afficher la page d'un tournoi

    Args:
        type_tournoi (str): Indique si le tournoi est "individuel" ou en "equipe"
        id_championnat (int): L'identifiant du tournoi dans la base de données
    """
    if type_tournoi == "individuel":
        champ = ChampionnatIndividuel.query.get(id_championnat)
        liste_dates = {}
        donnees = {}
    else:
        champ = ChampionnatEquipe.query.get(id_championnat)
        liste_dates = {}
        donnees = {}
        for participant in champ.participer:
            id_equipe = participant.equipe.id
            donnees[id_equipe] = {}
            liste_dates[id_equipe] = []
            for match in Affronter.query.filter(Affronter.championnat == champ,
                                                Affronter.equipe == participant.equipe):
                if match.date_match not in donnees[id_equipe]:
                    donnees[id_equipe][match.date_match] = match
                    if match.date_match not in liste_dates[id_equipe]:
                        liste_dates[id_equipe].append(match.date_match)
            liste_dates[id_equipe].sort()
    return render_template('tournoi.html', title="Tournoi - Competitions", championnat=champ,
                           type_champ=type_tournoi, matchs=donnees, dates=liste_dates)


@app.route('/competitions/tournoi/individuel/<int:id_championnat>/<int:id_joueur>/delete/',
           methods=('GET', 'POST'))
@login_required
def participant_indiv_delete(id_championnat: int, id_joueur: int):
    """Permet de supprimer un participant d'un tournoi individuel

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
        id_joueur (int): L'identifiant d'un joueur dans la base de données
    """
    joueur = Joueur.query.get(id_joueur)
    championnat = ChampionnatIndividuel.query.get(id_championnat)
    classer = Classer.query.get((id_championnat, id_joueur))
    un_joueur = Joueur.query.get(id_joueur)
    form = FormClasser(joueur=id_joueur, rang=classer.rang)
    form.joueur.choices = [(un_joueur.id, f"{un_joueur.prenom} {un_joueur.nom}")]
    if form.validate_on_submit():
        db.session.delete(classer)
        db.session.commit()
        return redirect(url_for("tournoi", type_tournoi="individuel",
                                id_championnat=id_championnat))
    return render_template('participant_indiv_delete.html', title="Supprimer un participant",
                           form=form, championnat=championnat, joueur=joueur)


@app.route('/competitions/tournoi/individuel/<int:id_championnat>/<int:id_joueur>/update/',
           methods=('GET', 'POST'))
@login_required
def participant_indiv_update(id_championnat: int, id_joueur: int):
    """Permet de modifier le résultat d'un participant lors d'un championnat individuel

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
        id_joueur (int): L'identifiant d'un joueur dans la base de données
    """
    joueur = Joueur.query.get(id_joueur)
    championnat = ChampionnatIndividuel.query.get(id_championnat)
    classer = Classer.query.get((id_championnat, id_joueur))
    un_joueur = Joueur.query.get(id_joueur)
    form = FormClasser(joueur=id_joueur, rang=classer.rang)
    form.joueur.choices = [(un_joueur.id, f"{un_joueur.prenom} {un_joueur.nom}")]
    if form.validate_on_submit():
        classer.rang = form.rang.data
        db.session.commit()
        return redirect(url_for("tournoi", type_tournoi="individuel",
                                id_championnat=id_championnat))
    return render_template('participant_indiv_update.html', title="Modifier un participant",
                           form=form, championnat=championnat, joueur=joueur)


@app.route('/competitions/tournoi/individuel/<int:id_championnat>/add/', methods=('GET', 'POST'))
@login_required
def participant_indiv_add(id_championnat: int):
    """Permet d'ajouter un participant à un tournoi individuel

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
    """
    championnat = ChampionnatIndividuel.query.get(id_championnat)
    les_joueurs = Joueur.query.filter(~Joueur.classer.any(\
        Classer.championnat.has(ChampionnatIndividuel.id == id_championnat)))
    choix = []
    for donnee in les_joueurs:
        choix.append((donnee.id, f"{donnee.prenom} {donnee.nom}"))
    form = FormClasser()
    form.joueur.choices = choix
    if form.validate_on_submit():
        classer = Classer(id_championnat=id_championnat, id_j=form.joueur.data,
                          rang=form.rang.data)
        db.session.add(classer)
        db.session.commit()
        return redirect(url_for("tournoi", type_tournoi="individuel",
                                id_championnat=id_championnat))
    return render_template('participant_indiv_add.html', title="Ajouter un participant",
                           form=form, championnat=championnat)


@app.route('/competitions/tournois-internes/')
def internes():
    return render_template('internes.html', title="Tournois internes - Competitions")
