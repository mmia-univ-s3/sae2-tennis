from datetime import datetime, date, timedelta
from operator import itemgetter

from flask import render_template, redirect, url_for
from sqlalchemy.exc import IntegrityError

from appli.app import app, db, required_permission_lvl
from appli.models import ChampionnatIndividuel, ChampionnatEquipe, Affronter, Joueur, Classer,\
Equipe, Participer, ChampionnatInterne, Jouer, Championnat, Opposer
from appli.forms import FormChampionnatEquipe, FormChampionnatIndividuel, FormClasser, \
    FormParticiper, FormAffronter, FormInternes, FormConfirm, FormMatch, FormMatchUpdate, \
    FormOpposer


@app.route('/competitions/calendrier/')
def calendrier():
    """Permet d'afficher la page concernant le calendrier des tournois"""
    premiere_date = date.today() - timedelta(days=(int(datetime.today().strftime("%w")) - 1) % 7)
    derniere_date = date.today() + timedelta(days=(-int(datetime.today().strftime("%w"))) % 7 + 21)
    list_comp_calendrier = Championnat.query.filter(Championnat.date_championnat.between(
        premiere_date.strftime("%Y-%m-%d"), derniere_date.strftime("%Y-%m-%d")
    )).all()
    date_jour = premiere_date
    list_dates = []
    dico_calendrier = {}
    num_jour = 0
    num_semaine = -1
    while date_jour <= derniere_date:
        if num_jour == 0:
            list_dates.append([])
            num_semaine += 1
        list_dates[num_semaine].append(date_jour)
        dico_calendrier[date_jour] = []
        num_jour = (num_jour + 1) % 7
        date_jour = date_jour + timedelta(days=1)
    for comp in list_comp_calendrier:
        dico_calendrier[comp.date_championnat].append(comp)
    list_comp_indiv = ChampionnatIndividuel.query.order_by(\
        ChampionnatIndividuel.date_championnat.desc()).all()
    list_comp_equipe = ChampionnatEquipe.query.order_by(\
        ChampionnatEquipe.date_championnat.desc()).all()
    list_comp = Championnat.query.order_by(Championnat.date_championnat)\
        .filter(Championnat.type_championnat != "interne").all()
    list_annees = []
    for comp in list_comp:
        if comp.type_championnat != "interne" and comp.date_championnat.year not in list_annees:
            list_annees.append(comp.date_championnat.year)
    return render_template('calendrier.html', title="Calendrier - Compétitions",
                           comp_indiv=list_comp_indiv, comp_equipe=list_comp_equipe,
                           calendrier=dico_calendrier, dates=list_dates, annees=list_annees,
                           annee=None)


@app.route('/competitions/calendrier/<int:annee>')
def calendrier_annee(annee):
    """Permet d'afficher la page concernant les tournois démarrant durant une certaine année

    Args:
        annee (int): L'année où les tournois ont commencés
    """
    list_comp_indiv = ChampionnatIndividuel.query.filter(
        ChampionnatIndividuel.date_championnat.between(f'{annee}-01-01', f'{annee}-12-31')
    ).order_by(\
        ChampionnatIndividuel.date_championnat.desc()).all()
    list_comp_equipe = ChampionnatEquipe.query.filter(
        ChampionnatIndividuel.date_championnat.between(f'{annee}-01-01', f'{annee}-12-31')
    ).order_by(\
        ChampionnatEquipe.date_championnat.desc()).all()
    list_comp = Championnat.query.order_by(Championnat.date_championnat).\
        filter(Championnat.type_championnat != "interne").all()
    list_annees = []
    for comp in list_comp:
        if comp.type_championnat != "interne" and comp.date_championnat.year not in list_annees:
            list_annees.append(comp.date_championnat.year)
    return render_template('calendrier.html', title="Calendrier - Compétitions",
                           comp_indiv=list_comp_indiv, comp_equipe=list_comp_equipe,
                           calendrier={}, dates=[], annees=list_annees, annee=annee)


@app.route('/competitions/tournoi/<int:id_championnat>/delete/',
           methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
def tournoi_delete(id_championnat: int):
    """Permet de supprimer un tournoi de la base de données

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
    """
    championnat = Championnat.query.get(id_championnat)
    if championnat.type_championnat == "individuel":
        form = FormChampionnatIndividuel(titre=championnat.titre,
                                         date_championnat=championnat.date_championnat,
                                         categorie=championnat.categorie, serie=championnat.serie,
                                         niveau=championnat.niveau)
    else:
        form = FormChampionnatEquipe(titre=championnat.titre,
                                     date_championnat=championnat.date_championnat,
                                     categorie=championnat.categorie, serie=championnat.serie)
    if form.validate_on_submit():
        db.session.delete(championnat)
        db.session.commit()
        return redirect(url_for("calendrier"))
    return render_template('tournoi_delete.html', title="Supprimer un tournoi", form=form,
                           type_tournoi=championnat.type_championnat, championnat=championnat)


@app.route('/competitions/tournoi/<int:id_championnat>/update/',
           methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
def tournoi_update(id_championnat: int):
    """Permet de modifier un tournoi de la base de données

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
    """
    championnat = Championnat.query.get(id_championnat)
    if championnat.type_championnat == "individuel":
        form = FormChampionnatIndividuel(titre=championnat.titre,
                                         date_championnat=championnat.date_championnat,
                                         categorie=championnat.categorie, serie=championnat.serie,
                                         niveau=championnat.niveau)
    else:
        form = FormChampionnatEquipe(titre=championnat.titre,
                                     date_championnat=championnat.date_championnat,
                                     categorie=championnat.categorie, serie=championnat.serie)
    if form.validate_on_submit():
        championnat.titre = form.titre.data
        championnat.date_championnat = form.date_championnat.data
        championnat.categorie = form.categorie.data
        championnat.serie = form.serie.data
        if championnat.type_championnat == "individuel":
            championnat.niveau = form.niveau.data
        db.session.commit()
        return redirect(url_for("calendrier"))
    return render_template('tournoi_update.html', title="Modifier un tournoi", form=form,
                           type_tournoi=championnat.type_championnat, championnat=championnat)


@app.route('/competitions/tournoi/<type_tournoi>/add/', methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
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


@app.route('/competitions/tournoi/<int:id_championnat>/')
def tournoi(id_championnat: int):
    """Permet d'afficher la page d'un tournoi

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
    """
    liste_dates = {}
    donnees = {}
    champ = Championnat.query.get(id_championnat)
    if champ.type_championnat == "individuel":
        for classement in champ.classer:
            id_joueur = classement.joueur.id
            donnees[id_joueur] = {}
            liste_dates[id_joueur] = []
            for match in Opposer.query.filter(Opposer.championnat == champ,
                                              Opposer.joueur == classement.joueur):
                if match.date_match not in donnees[id_joueur]:
                    donnees[id_joueur][match.date_match] = match
                    if match.date_match not in liste_dates[id_joueur]:
                        liste_dates[id_joueur].append(match.date_match)
            liste_dates[id_joueur].sort()
    else:
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
                           type_champ=champ.type_championnat, matchs=donnees, dates=liste_dates)


@app.route('/competitions/tournoi/<int:id_championnat>/<int:id_participant>/delete/',
           methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
def participant_delete(id_championnat: int, id_participant: int):
    """Permet de supprimer un participant d'un tournoi

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
        id_participant (int): L'identifiant d'un joueur ou d'une équipe dans la base de données
    """
    championnat = Championnat.query.get(id_championnat)
    if championnat.type_championnat == "individuel":
        joueur = Joueur.query.get(id_participant)
        classer = Classer.query.get((id_championnat, id_participant))
        form = FormClasser(joueur=id_participant, rang=classer.rang)
        form.joueur.choices = [(joueur.id, f"{joueur.prenom} {joueur.nom}")]
        form.joueur.data = joueur.id
        if form.validate_on_submit():
            db.session.delete(classer)
            db.session.commit()
            return redirect(url_for("tournoi", id_championnat=id_championnat))
        return render_template('participant_indiv_delete.html', title="Supprimer un participant",
                               form=form, championnat=championnat, joueur=joueur)
    equipe = Equipe.query.get(id_participant)
    participer = Participer.query.get((id_championnat, id_participant))
    form = FormParticiper(joueur=id_participant, rang=participer.rang, poule=participer.poule)
    form.equipe.choices = [(equipe.id, equipe.nom)]
    form.equipe.data = equipe.id
    if form.validate_on_submit():
        db.session.delete(participer)
        db.session.commit()
        return redirect(url_for("tournoi", id_championnat=id_championnat))
    return render_template('participant_equipe_delete.html', title="Supprimer une équipe",
                            form=form, championnat=championnat, equipe=equipe)


@app.route('/competitions/tournoi/<int:id_championnat>/<int:id_participant>/update/',
           methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
def participant_update(id_championnat: int, id_participant: int):
    """Permet de modifier le résultat d'un participant lors d'un championnat

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
        id_participant (int): L'identifiant d'un joueur ou d'une équipe dans la base de données
    """
    championnat = Championnat.query.get(id_championnat)
    if championnat.type_championnat == "individuel":
        joueur = Joueur.query.get(id_participant)
        classer = Classer.query.get((id_championnat, id_participant))
        form = FormClasser(joueur=id_participant, rang=classer.rang)
        form.joueur.choices = [(joueur.id, f"{joueur.prenom} {joueur.nom}")]
        if form.validate_on_submit():
            classer.rang = form.rang.data
            db.session.commit()
            return redirect(url_for("tournoi", id_championnat=id_championnat))
        return render_template('participant_indiv_update.html', title="Modifier un participant",
                              form=form, championnat=championnat, joueur=joueur)
    equipe = Equipe.query.get(id_participant)
    participer = Participer.query.get((id_championnat, id_participant))
    form = FormParticiper(equipe=id_participant, rang=participer.rang, poule=participer.poule)
    form.equipe.choices = [(equipe.id, equipe.nom)]
    if form.validate_on_submit():
        participer.rang = form.rang.data
        participer.poule = form.poule.data
        db.session.commit()
        return redirect(url_for("tournoi", id_championnat=id_championnat))
    return render_template('participant_equipe_update.html', title="Modifier une équipe",
                        form=form, championnat=championnat, equipe=equipe)


@app.route('/competitions/tournoi/<int:id_championnat>/add/', methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
def participant_add(id_championnat: int):
    """Permet d'ajouter un participant à un tournoi

    Args:
        id_championnat (int): L'identifiant du tournoi dans la base de données
    """
    championnat = Championnat.query.get(id_championnat)
    if championnat.type_championnat == "individuel":
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
            return redirect(url_for("tournoi", id_championnat=id_championnat))
        return render_template('participant_indiv_add.html', title="Ajouter un participant",
                               form=form, championnat=championnat)
    les_equipes = Equipe.query.filter(~Equipe.participer.any(\
        Participer.championnat.has(ChampionnatEquipe.id == id_championnat)),
        Equipe.saison == championnat.date_championnat.year)
    choix = []
    for donnee in les_equipes:
        choix.append((donnee.id, donnee.nom))
    form = FormParticiper()
    form.equipe.choices = choix
    if form.validate_on_submit():
        participer = Participer(id_championnat=id_championnat, id_equipe=form.equipe.data,
                                rang=form.rang.data, poule=form.poule.data)
        db.session.add(participer)
        db.session.commit()
        return redirect(url_for("tournoi", id_championnat=id_championnat))
    return render_template('participant_equipe_add.html', title="Ajouter une équipe",
                        form=form, championnat=championnat)


@app.route('/competitions/tournoi/<int:id_championnat>/<int:id_participant>/<date_match>/'\
           + 'delete/', methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
def affronter_delete(id_championnat: int, id_participant: int, date_match: str):
    """Supprime un affrontement entre 2 participants d'un championnat.

    Args :
        id_championnat (int): L'identifiant du championnat.
        id_participant (int): L'identifiant du participant.
        date_match (str): La date du match.
    """
    championnat = Championnat.query.get(id_championnat)
    if championnat.type_championnat == "individuel":
        date_str = datetime.strptime(date_match, "%d-%m-%Y").date()
        opposer = Opposer.query.get((id_championnat, id_participant, date_str))
        form = FormOpposer()
        form.adversaire.data = opposer.adversaire
        form.date.data = date_str
        form.resultat.data = opposer.resultat
        form.score.data = opposer.score
        form.domicile.data = str(opposer.domicile)
        if form.validate_on_submit():
            db.session.delete(opposer)
            db.session.commit()
            return redirect(url_for("tournoi", id_championnat=id_championnat))
        return render_template('opposer_delete.html', title="Supprimer un match",
                            form=form, championnat=opposer.championnat, joueur=opposer.joueur,
                            adversaire=opposer.adversaire, date_match=date_str)
    date_str = datetime.strptime(date_match, "%d-%m-%Y").date()
    affronter = Affronter.query.get((id_championnat, id_participant, date_str))
    form = FormAffronter()
    form.adversaire.data = affronter.adversaire
    form.date.data = date_str
    form.resultat.data = affronter.resultat
    form.score.data = affronter.score
    form.domicile.data = str(affronter.domicile)
    if form.validate_on_submit():
        db.session.delete(affronter)
        db.session.commit()
        return redirect(url_for("tournoi", id_championnat=id_championnat))
    return render_template('affronter_delete.html', title="Supprimer un match",
                        form=form, championnat=affronter.championnat, equipe=affronter.equipe,
                        adversaire=affronter.adversaire, date_match=date_str)


@app.route('/competitions/tournoi/<int:id_championnat>/<int:id_participant>/<date_match>/'\
           + 'update/', methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
def affronter_update(id_championnat: int, id_participant: int, date_match: str):
    """Met à jour un affrontement entre 2 équipes.
    Args :
        id_championnat (int): L'identifiant du championnat.
        id_participant (int): L'identifiant de l'équipe.
        date_match (str): La date du match.
    """
    championnat = Championnat.query.get(id_championnat)
    try:
        if championnat.type_championnat == "individuel":
            date_str = datetime.strptime(date_match, "%d-%m-%Y").date()
            opposer = Opposer.query.get((id_championnat, id_participant, date_str))
            form = FormOpposer(date=date_str, score=opposer.score, domicile=str(opposer.domicile),
                                resultat=opposer.resultat, mise_avant=opposer.mise_avant)
            form.adversaire.data = opposer.adversaire
            if form.validate_on_submit():
                opposer.date_match = form.date.data
                opposer.resultat = form.resultat.data
                opposer.score = form.score.data
                opposer.domicile = form.domicile.data == 'True'
                opposer.mise_avant = form.mise_avant.data
                db.session.commit()
                return redirect(url_for("tournoi", id_championnat=id_championnat))
            return render_template('opposer_update.html', title="Modifier un match",
                                   form=form, championnat=opposer.championnat,
                                   joueur=opposer.joueur,
                                   adversaire=opposer.adversaire, date_match=date_match)
        date_str = datetime.strptime(date_match, "%d-%m-%Y").date()
        affronter = Affronter.query.get((id_championnat, id_participant, date_str))
        form = FormAffronter(date=date_str, score=affronter.score,
                                domicile=str(affronter.domicile),
                                resultat=affronter.resultat)
        form.adversaire.data = affronter.adversaire
        if form.validate_on_submit():
            affronter.date_match = form.date.data
            affronter.resultat = form.resultat.data
            affronter.score = form.score.data
            affronter.domicile = form.domicile.data == 'True'
            affronter.mise_avant = form.mise_avant.data
            db.session.commit()
            return redirect(url_for("tournoi", id_championnat=id_championnat))
        return render_template('affronter_update.html', title="Modifier un match",
                                form=form, championnat=affronter.championnat,
                                equipe=affronter.equipe,
                                adversaire=affronter.adversaire, date_match=date_match)
    except IntegrityError:
        db.session.rollback()
        if championnat.type_championnat == "individuel":
            return render_template('opposer_update.html', title="Modifier un match",
                                   form=form, championnat=opposer.championnat,
                                   joueur=opposer.joueur, adversaire=opposer.adversaire,
                                   date_match=date_str)
        return render_template('affronter_update.html', title="Modifier un match",
                               form=form, championnat=affronter.championnat,
                               equipe=affronter.equipe,
                               adversaire=affronter.adversaire, date_match=date_str)


@app.route('/competitions/tournoi/<int:id_championnat>/<int:id_participant>/add/',
           methods=('GET', 'POST'))
@required_permission_lvl("publicateur")
def affronter_add(id_championnat: int, id_participant: int):
    """Ajoute un affrontement.

    Args:
        id_championnat (int): L'identifiant du championnat.
        id_equipe (int): L'identifiant de l'équipe."""
    championnat = Championnat.query.get(id_championnat)
    try:
        if championnat.type_championnat == "individuel":
            joueur = Joueur.query.get(id_participant)
            form = FormOpposer()
            if form.validate_on_submit():
                opposer = Opposer(id_championnat=id_championnat, id_joueur=id_participant,
                                    adversaire=form.adversaire.data, resultat=form.resultat.data,
                                    score=form.score.data, domicile=form.domicile.data == 'True',
                                    date_match=form.date.data, mise_avant=form.mise_avant.data)
                db.session.add(opposer)
                db.session.commit()
                return redirect(url_for("tournoi", id_championnat=id_championnat))
            return render_template('opposer_add.html', title="Ajouter un match",
                                form=form, championnat=championnat, joueur=joueur)
        equipe = Equipe.query.get(id_participant)
        form = FormAffronter()
        if form.validate_on_submit():
            affronter = Affronter(id_championnat=id_championnat, id_equipe=id_participant,
                                adversaire=form.adversaire.data, resultat=form.resultat.data,
                                score=form.score.data, domicile=form.domicile.data == 'True',
                                date_match=form.date.data, mise_avant=form.mise_avant.data)
            db.session.add(affronter)
            db.session.commit()
            return redirect(url_for("tournoi", id_championnat=id_championnat))
        return render_template('affronter_add.html', title="Ajouter un match",
                            form=form, championnat=championnat, equipe=equipe)
    except IntegrityError:
        db.session.rollback()
        if championnat.type_championnat == "individuel":
            return render_template('opposer_add.html', title="Ajouter un match",
                                   form=form, championnat=championnat, joueur=joueur)
        return render_template('affronter_add.html', title="Ajouter un match",
                               form=form, championnat=championnat, equipe=equipe)


@app.route('/competitions/palmares/list/')
def palmares_list():
    """Affiche la liste des palmarès."""
    liste_championnat = Championnat.query.filter(Championnat.type_championnat != "interne")\
        .order_by(Championnat.date_championnat.desc()).all()
    liste_annee = []
    for championnat in liste_championnat:
        if championnat.date_championnat.year not in liste_annee:
            liste_annee.append(championnat.date_championnat.year)
    return render_template('palmares_liste.html', title="Palmarès - Competitions",
                           liste_annee=liste_annee)


@app.route('/competitions/palmares/<int:annee>/')
def palmares_annee(annee: int):
    """Page affichant le palmarès du club durant une année donnée

    Args:
        annee (int): L'année
    """
    liste_champ_indiv = ChampionnatIndividuel.query.filter(
        ChampionnatIndividuel.date_championnat.between(f'{annee}-01-01', f'{annee}-12-31')).all()
    dict_indiv = {}
    for championnat in liste_champ_indiv:
        dict_indiv.setdefault(championnat.niveau, {})
        dict_indiv[championnat.niveau].setdefault(championnat.categorie, set())
        dict_indiv[championnat.niveau][championnat.categorie].add(championnat)

    liste_champ_equipe = ChampionnatEquipe.query.filter(
        ChampionnatEquipe.date_championnat.between(f'{annee}-01-01', f'{annee}-12-31')).all()
    dict_equipe = {}
    for championnat in liste_champ_equipe:
        dict_equipe.setdefault(championnat.categorie, {})
        dict_equipe[championnat.categorie].setdefault(championnat, set())
        for participation in championnat.participer:
            participation:Participer
            dict_equipe[championnat.categorie][championnat].add(participation)

    return render_template('palmares.html',
                           title=f"Palmarès {annee} - Competitions", annee=annee, indiv=dict_indiv,
                           equipe=dict_equipe)


@app.route('/competitions/tournois-internes/')
def internes():
    """ Page de la liste des tournois en interne """
    tournois = ChampionnatInterne.query.order_by(ChampionnatInterne.date_championnat)
    return render_template('internes.html',
                           title="Tournois internes - Competitions", tournois=tournois)

@app.route('/competitions/tournois-internes/add/', methods=['GET', 'POST'])
@required_permission_lvl("publicateur")
def interne_add():
    """Page permettant d'ajouter un tournoi interne"""
    form = FormInternes()
    if form.validate_on_submit():
        interne = ChampionnatInterne(form.date.data, form.titre.data)
        db.session.add(interne)
        db.session.commit()
        return redirect(url_for("internes"))
    return render_template('interne_add.html', title="Ajout d'un tournoi interne",
                           form=form)

@app.route('/competitions/tournois-internes/delete/<int:id_interne>/', methods=['GET', 'POST'])
@required_permission_lvl("publicateur")
def interne_delete(id_interne):
    """Page permettant de supprimer un tournoi interne"""
    tournoi_interne = ChampionnatInterne.query.get(id_interne)
    form = FormConfirm()
    if form.validate_on_submit() and tournoi_interne is not None:
        db.session.delete(tournoi_interne)
        db.session.commit()
        return redirect(url_for("internes"))
    return render_template('interne_delete.html',
                           title="Suppression d'un tournoi interne", form=form,
                           interne=tournoi_interne)


@app.route('/competitions/tournois-internes/<int:id_interne>/', methods=['GET', 'POST'])
def interne_view(id_interne):
    """Page permettant de visualiser/modifier un tournoi interne"""
    tournoi_interne = ChampionnatInterne.query.get(id_interne)
    # pylint: disable=protected-access
    liste_matchs = Jouer.query.filter(Jouer._id_championnat == tournoi_interne.id).all()
    matchs = []
    for match in liste_matchs:
        joueur1 = match.joueur1
        joueur2 = match.joueur2
        score1 = match.sets_gagnees_j1()
        score2 = match.sets_gagnees_j2()
        matchs.append((tournoi_interne, joueur1, score1, joueur2, score2))

    classer = []
    nb_victoires = nb_victoires_by_player(id_interne)
    for joueur, wins in nb_victoires.items():
        classer.append((joueur,wins))
    classement = sorted(classer, key=itemgetter(1), reverse=True)

    form = FormInternes(date=tournoi_interne.date_championnat, titre=tournoi_interne.titre)
    if form.validate_on_submit():
        tournoi_interne.date = form.date.data
        tournoi_interne.titre = form.titre.data
        db.session.commit()
        return redirect(url_for("internes", id_interne=id_interne))
    return render_template("interne_view.html", title="Tournoi interne",
                           interne=tournoi_interne, form=form, matchs=matchs,
                           id_interne=id_interne, classement=classement)

@app.route('/competitions/tournois-internes/<int:id_interne>/<int:id_j1>/<int:id_j2>/',
           methods=['GET', 'POST'])
@required_permission_lvl("publicateur")
def match_update(id_interne, id_j1, id_j2):
    """Page permettant de modifier un match d'un tournoi interne"""
    tournoi_interne = ChampionnatInterne.query.get(id_interne)
    match = Jouer.query.get((id_interne, id_j1, id_j2))
    id_joueurs = (id_j1, id_j2)
    form = FormMatchUpdate(sets=match.sets, points1=match.score1, points2=match.score2)

    if form.validate_on_submit():
        if len(form.points1.data) == len(form.points2.data):
            match.score1 = form.points1.data
            match.score2 = form.points2.data
            db.session.commit()
            return redirect(url_for("interne_view", id_interne=id_interne))
        return render_template("interne_match_update.html",
                               title="Modification d'un match", form=form, interne=tournoi_interne,
                               id_joueurs=id_joueurs, error=True, id_interne=id_interne)
    return render_template('interne_match_update.html',
                           title="Modification d'un match", form=form, interne=tournoi_interne,
                           error=False, match=match, id_joueurs=id_joueurs, id_interne=id_interne)


@app.route('/competitions/tournois-internes/<int:id_interne>/add/', methods=['GET', 'POST'])
@required_permission_lvl("publicateur")
def match_add(id_interne):
    """Page permettant d'ajouter un match dans un tournoi interne"""
    tournoi_interne = ChampionnatInterne.query.get(id_interne)
    form = FormMatch()

    # Liste déroulante des joueurs
    joueurs = Joueur.query.all()
    choix = []
    for joueur in joueurs:
        choix.append((joueur.id, joueur.prenom + " " + joueur.nom))

    form.joueur1.choices = choix
    form.joueur2.choices = choix

    if form.validate_on_submit():
        if len(form.points1.data) == len(form.points2.data) and form.joueur1 != form.joueur2:
            match = Jouer(id_interne, form.joueur1.data, form.joueur2.data, form.sets.data,
                          form.points1.data, form.points2.data)
            db.session.add(match)
            db.session.commit()
            return redirect(url_for("interne_view", id_interne=id_interne))
        return render_template("interne_match_add.html", title="Ajout d'un match",
                               form=form, interne=tournoi_interne, error=True)
    return render_template('interne_match_add.html', title="Ajout d'un match",
                           form=form, interne=tournoi_interne, error=False)

@app.route('/competitions/tournois-internes/delete/<int:id_interne>/<int:id_j1>/<int:id_j2>',
           methods=['GET', 'POST'])
@required_permission_lvl("publicateur")
def match_delete(id_interne, id_j1, id_j2):
    """Page permettant de supprimer un match dans un tournoi interne"""
    match = Jouer.query.get((id_interne, id_j1, id_j2))
    id_joueurs = (id_j1, id_j2)
    form = FormConfirm()
    if form.validate_on_submit() and match is not None:
        db.session.delete(match)
        db.session.commit()
        return redirect(url_for("interne_view", id_interne=id_interne))
    return render_template('interne_match_delete.html',
                           title="Suppression d'un match d'un tournoi interne", form=form,
                           match=match, id_joueurs=id_joueurs)


def nb_victoires_by_player(id_interne):
    """Méthode pour réaliser le classement"""
    # pylint: disable=protected-access
    matchs = Jouer.query.filter(Jouer._id_championnat == id_interne).all()
    nb_victoires_joueurs = {}
    for match in matchs:
        if match.joueur1 not in nb_victoires_joueurs:
            nb_victoires_joueurs[f"{match.joueur1.prenom} {match.joueur1.nom}"] = 0
        if match.joueur2 not in nb_victoires_joueurs:
            nb_victoires_joueurs[f"{match.joueur2.prenom} {match.joueur2.nom}"] = 0
        if match.score1 > match.score2:
            nb_victoires_joueurs[f"{match.joueur1.prenom} {match.joueur1.nom}"] = (
                    nb_victoires_joueurs.get(f"{match.joueur1.prenom} {match.joueur1.nom}") + 1)
        if match.score2 > match.score1:
            nb_victoires_joueurs[f"{match.joueur2.prenom} {match.joueur2.nom}"] = (
                    nb_victoires_joueurs.get(f"{match.joueur2.prenom} {match.joueur2.nom}") + 1)
    return nb_victoires_joueurs
