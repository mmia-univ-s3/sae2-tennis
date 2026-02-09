import csv
import logging as lg
from datetime import date

import click

from .app import app, db
from .models import Article, Histoire, Partenaire, Utilisateur, CategorieTarif, Reservation, \
    Reduction, Division, ChampionnatEquipe, ChampionnatIndividuel, Equipe, Participer, \
    Affronter, Joueur, Classer, Sport


def _importer_articles(filename):
    """Permet d'importer les articles"""
    with open(filename, newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            article = Article(titre=ligne["titreArt"], image=ligne["image"],
                              contenu=ligne["contenu"],
                              date_publi=date.fromisoformat(ligne["dateArt"]),
                              type_article=ligne["typeArt"])
            db.session.add(article)
    db.session.commit()


def _importer_trivias(filename):
    """Permet d'importer les trivias liés à l'histoire du club"""
    with open(filename, newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            histoire = Histoire(annee=int(ligne["annee"]),
                                trivia=ligne["trivia"],
                                article=int(ligne["article"]) if ligne["article"] != "" else None)
            db.session.add(histoire)
    db.session.commit()


def _importer_partenaires(filename):
    """Permet d'importer les partenaires du club"""
    with open(filename, newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            partenaire = Partenaire(nom=ligne["nomP"], logo=ligne["logo"], lien=ligne["lien"], important=ligne["important"]=="True")
            db.session.add(partenaire)
    db.session.commit()


def _importer_users(filename):
    """Permet d'importer les utilisateurs"""
    with open(filename, newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            utilisateur = Utilisateur(login=ligne["idU"], mdp=ligne["mdp"])
            db.session.add(utilisateur)
    db.session.commit()


def _importer_tarifs(filepath):
    """Permet d'importer les tarifs"""
    with open(filepath + "/sport.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            sport = Sport(nom=ligne["nom"], commentaire=ligne["commentaire"])
            db.session.add(sport)

    with open(filepath + "/categorie.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            categorie = CategorieTarif(ordre=int(ligne["ordreCat"]),
                                       intitule=ligne["intituleCat"],
                                       id_sport=int(ligne["idSport"]),
                                       id_parent=int(ligne["idCatParent"])\
                                       if ligne["idCatParent"] != "" else None)
            db.session.add(categorie)

    with open(filepath + "/reservation.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            reservation = Reservation(ordre=int(ligne["ordreT"]), intitule=ligne["intituleT"],
                                      id_cat=int(ligne["idCat"]), montant=float(ligne["montant"]))
            reservation.id = int(ligne["idT"])
            db.session.add(reservation)

    with open(filepath + "/reduction.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            reduction = Reduction(ordre=int(ligne["ordreT"]), intitule=ligne["intituleT"],
                                  id_cat=int(ligne["idCat"]), taux=ligne["taux"],
                                  licence=ligne["surLicence"].strip() == "True")
            reduction.id = int(ligne["idT"])
            db.session.add(reduction)
    db.session.commit()


def _importer_championnats_equipes(filepath):
    """Permet d'importer les données relatives aux championnats par équipes"""
    with open(filepath + "/division.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            division = Division(intitule=ligne["intituleDiv"])
            db.session.add(division)

    with open(filepath + "/champ_equipe.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            champ = ChampionnatEquipe(date_championnat=date.fromisoformat(ligne["dateCha"]),
                                      titre=ligne["titreCha"], categorie=ligne["categorieSport"],
                                      serie=ligne["serie"])
            champ.id = int(ligne["idCha"])
            db.session.add(champ)

    with open(filepath + "/equipe.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            equipe = Equipe(nom=ligne["nomE"], saison=int(ligne["saison"]),
                            categorie=ligne["categorieE"], id_div=int(ligne["idDiv"]),
                            rang=ligne["rangDiv"])
            db.session.add(equipe)

    with open(filepath + "/participer.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            participer = Participer(id_championnat=int(ligne["idCha"]), id_equipe=int(ligne["idE"]),
                                    rang=ligne["rang"], poule=ligne["poule"])
            db.session.add(participer)

    with open(filepath + "/affronter.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            affronter = Affronter(id_championnat=int(ligne["idCha"]),
                                  id_equipe=int(ligne["idE"]),
                                  adversaire=ligne["nomAdv"],
                                  resultat=ligne["resultat"], score=ligne["score"],
                                  domicile=ligne["estDomicile"] == "True",
                                  date_match=date.fromisoformat(ligne["dateMatch"]))
            db.session.add(affronter)
    db.session.commit()


def _importer_championnats_individuels(filepath):
    """Permet d'importer les données relatives aux championnats individuels"""
    with open(filepath + "/joueur.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            joueur = Joueur(nom=ligne["nomJ"], prenom=ligne["prenomJ"],
                            id_equipe=int(ligne["idE"]) if ligne['idE'] != "" else None)
            db.session.add(joueur)

    with open(filepath + "/champ_indiv.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            champ = ChampionnatIndividuel(date_championnat=date.fromisoformat(ligne["dateCha"]),
                                          titre=ligne["titreCha"],
                                          categorie=ligne["categorieSport"], serie=ligne["serie"],
                                          niveau=ligne["niveau"],
                                          id_joueur_1=ligne["idJ1"],
                                          id_joueur_2=ligne["idJ2"],
                                          score_1=ligne["score1"],
                                          score_2=ligne["score2"])
            champ.id = int(ligne["idCha"])
            db.session.add(champ)

    with open(filepath + "/classer.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            classer = Classer(id_championnat=int(ligne["idCha"]), id_j=int(ligne["idJ"]),
                              rang=ligne["rang"])
            db.session.add(classer)
    db.session.commit()

# pylint: disable=protected-access
def _exporter_articles(filepath):
    """Permet d'exporter les articles"""
    liste_articles = Article.query.all()
    with open(f"{filepath}/article.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idArt", "titreArt", "image", "contenu", "nbClics", "dateArt", "typeArt"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for article in liste_articles:
            ecriture.writerow({"idArt" : str(article.id),
                               "titreArt" : article.titre,
                               "image" : article.image,
                               "contenu" : article.contenu,
                               "nbClics" : str(article.clics),
                               "dateArt" : article.date_publi.strftime("%Y-%m-%d"),
                               "typeArt" : article.type_article})

# pylint: disable=protected-access
def _exporter_trivias(filepath):
    """Permet d'exporter les trivias liés à l'histoire du club"""
    liste_trivias = Histoire.query.all()
    with open(f"{filepath}/histoire.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idH", "annee", "trivia", "article"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for trivia in liste_trivias:
            ecriture.writerow({"idH" : str(trivia.id),
                               "annee" : str(trivia.annee),
                               "trivia" : trivia.trivia,
                               "article" : "" if trivia.article is None else str(trivia.article)})

# pylint: disable=protected-access
def _exporter_partenaires(filepath):
    """Permet d'exporter les partenaires du club"""
    liste_partenaires = Partenaire.query.all()
    with open(f"{filepath}/partenaire.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idP", "nomP", "logo", "lien"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for partenaire in liste_partenaires:
            ecriture.writerow({"idP" : str(partenaire.id),
                               "nomP" : partenaire.nom,
                               "logo" : partenaire.logo,
                               "lien" : partenaire.lien})

# pylint: disable=protected-access
def _exporter_users(filepath):
    """Permet d'exporter les utilisateurs"""
    liste_utilisateurs = Utilisateur.query.all()
    with open(f"{filepath}/utilisateur.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idU", "mdp"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for utilisateur in liste_utilisateurs:
            ecriture.writerow({"idU" : utilisateur.login,
                               "mdp" : utilisateur.mdp})

# pylint: disable=protected-access
def _exporter_tarifs(filepath):
    """Permet d'exporter les tarifs"""
    liste_sports = Sport.query.all()
    with open(f"{filepath}/sport.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idSport", "nom", "commentaire"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for sport in liste_sports:
            ecriture.writerow({"idSport" : str(sport.id),
                               "nom" : sport.nom,
                               "commentaire" : sport.commentaire})

    liste_categories = CategorieTarif.query.all()
    with open(f"{filepath}/categorie.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idCat", "ordreCat", "intituleCat", "idSport", "idCatParent"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for categorie in liste_categories:
            ecriture.writerow({"idCat" : str(categorie.id),
                               "ordreCat" : str(categorie.ordre),
                               "intituleCat" : categorie.intitule,
                               "idSport" : str(categorie._id_sport),
                               "idCatParent" : "" if categorie._id_parent is None\
                                else str(categorie._id_parent)})


    liste_reservations = Reservation.query.all()
    with open(f"{filepath}/reservation.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idT", "ordreT", "intituleT", "idCat", "montant"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for reservation in liste_reservations:
            ecriture.writerow({"idT" : str(reservation.id),
                               "ordreT" : str(reservation.ordre),
                               "intituleT" : reservation.intitule,
                               "idCat" : str(reservation._id_cat),
                               "montant" : str(reservation.montant)})


    liste_reductions = Reduction.query.all()
    with open(f"{filepath}/reduction.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idT", "ordreT", "intituleT", "idCat", "taux", "surLicence"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for reduction in liste_reductions:
            ecriture.writerow({"idT" : str(reduction.id),
                               "ordreT" : str(reduction.ordre),
                               "intituleT" : reduction.intitule,
                               "idCat" : str(reduction._id_cat),
                               "taux" : reduction.taux,
                               "surLicence" : str(reduction.licence)})

# pylint: disable=protected-access
def _exporter_championnats_equipes(filepath):
    """Permet d'exporter les données relatives aux championnats par équipes"""
    liste_divisions = Division.query.all()
    with open(f"{filepath}/division.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idDiv", "intituleDiv"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for division in liste_divisions:
            ecriture.writerow({"idDiv" : str(division.id),
                               "intituleDiv" : division.intitule})

    liste_championnat = ChampionnatEquipe.query.all()
    with open(f"{filepath}/champ_equipe.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idCha", "dateCha", "titreCha", "categorieSport", "serie"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for championnat in liste_championnat:
            ecriture.writerow({"idCha" : str(championnat.id),
                               "dateCha" : championnat.date_championnat.strftime("%Y-%m-%d"),
                               "titreCha" : championnat.titre,
                               "categorieSport" : championnat.categorie,
                               "serie" : championnat.serie})

    liste_equipes = Equipe.query.all()
    with open(f"{filepath}/equipe.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idE", "nomE", "saison", "categorieE", "idDiv", "rangDiv"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for equipe in liste_equipes:
            ecriture.writerow({"idE" : str(equipe.id),
                               "nomE" : equipe.nom,
                               "saison" : str(equipe.saison),
                               "categorieE" : equipe.categorie,
                               "idDiv" : str(equipe._id_div),
                               "rangDiv" : equipe.rang})

    liste_participants = Participer.query.all()
    with open(f"{filepath}/participer.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idCha", "idE", "rang", "poule"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for participant in liste_participants:
            ecriture.writerow({"idCha" : str(participant._id_championnat),
                               "idE" : str(participant._id_equipe),
                               "rang" : participant.rang,
                               "poule" : participant.poule})

    liste_matchs = Affronter.query.all()
    with open(f"{filepath}/affronter.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idCha", "idE", "nomAdv", "resultat", "score", "estDomicile", "dateMatch"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for match in liste_matchs:
            ecriture.writerow({"idCha" : str(match._id_championnat),
                               "idE" : str(match._id_equipe),
                               "nomAdv" : match.adversaire,
                               "resultat" : match.resultat,
                               "score" : match.score,
                               "estDomicile" : str(match.domicile),
                               "dateMatch" : match.date_match.strftime("%Y-%m-%d")})

# pylint: disable=protected-access
def _exporter_championnats_individuels(filepath):
    """Permet d'exporter les données relatives aux championnats individuels"""
    liste_joueurs = Joueur.query.all()
    with open(f"{filepath}/joueur.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idJ", "nomJ", "prenomJ", "idE"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for joueur in liste_joueurs:
            ecriture.writerow({"idJ" : str(joueur.id),
                               "nomJ" : joueur.nom,
                               "prenomJ" : joueur.prenom,
                               "idE" : "" if joueur._id_equipe is None\
                                else str(joueur._id_equipe)})

    liste_championnats = ChampionnatIndividuel.query.all()
    with open(f"{filepath}/champ_indiv.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idCha", "dateCha", "titreCha", "categorieSport", "serie", "niveau",
                    "idJ1", "idJ2", "score1", "score2"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        for championnat in liste_championnats:
            ecriture.writerow({"idCha" : str(championnat.id),
                               "dateCha" : championnat.date_championnat.strftime("%Y-%m-%d"),
                               "titreCha" : championnat.titre,
                               "categorieSport" : championnat.categorie,
                               "serie" : championnat.serie,
                               "niveau" : championnat.niveau,
                               "idJ1" : "" if championnat._id_joueur_1 is None\
                                else str(championnat._id_joueur_1),
                               "idJ2" : "" if championnat._id_joueur_2 is None\
                                else str(championnat._id_joueur_2),
                               "score1" : "" if championnat.score_1 is None\
                                else str(championnat.score_1),
                               "score2" : "" if championnat.score_2 is None\
                                else str(championnat.score_2)})

    liste_classements = Classer.query.all()
    with open(f"{filepath}/classer.csv", 'w', newline="", encoding="utf-8") as csvfile:
        colonnes = ["idCha", "idJ", "rang"]
        ecriture : csv.DictWriter = csv.DictWriter(csvfile, fieldnames=colonnes, delimiter=';')
        ecriture.writeheader()
        liste_classements:list[Classer]
        for classement in liste_classements:
            ecriture.writerow({"idCha" : str(classement._id_championnat),
                               "idJ" : str(classement._id_j),
                               "rang" : classement.rang})


@app.cli.command()
@click.argument('filepath')
def loaddb(filepath):
    """Crée les tables de la base et les remplies

    Args:
        filepath (str): Le chemin du dossier contenant les fichiers CSV où se trouvent les données
                        de notre base
    """
    #  création de toutes les tables
    db.drop_all()
    db.create_all()

    try:
        _importer_articles(filename=filepath + "/article.csv")
        lg.info('Articles importés')

        _importer_trivias(filename=filepath + "/histoire.csv")
        lg.info('Trivias importées')

        _importer_partenaires(filename=filepath + "/partenaire.csv")
        lg.info('Partenaires importés')

        _importer_users(filename=filepath + "/utilisateur.csv")
        lg.info('Utilisateurs importés')

        _importer_tarifs(filepath=filepath)
        lg.info('Tarifs importés')

        _importer_championnats_equipes(filepath=filepath)
        lg.info('Championnats par équipes importés')

        _importer_championnats_individuels(filepath=filepath)
        lg.info('Championnats individuels importés')

        lg.info('Base de données créée')

    except FileNotFoundError as err:
        lg.error("FileNotFoundError: %s", err)
    except NotADirectoryError as err:
        lg.error("NotADirectoryError: %s", err)
    except PermissionError as err:
        lg.error("PermissionError: %s", err)


@app.cli.command()
@click.argument('filepath')
def savedb(filepath):
    """Exportes les éléments stockés dans la base de données dans des fichiers csv

    Args:
        filepath (str): Le chemin du dossier où seront stockés les données
    """
    try:
        _exporter_articles(filepath=filepath)
        lg.info('Articles exportés')

        _exporter_trivias(filepath=filepath)
        lg.info('Trivias exportées')

        _exporter_partenaires(filepath=filepath)
        lg.info('Partenaires exportés')

        _exporter_users(filepath=filepath)
        lg.info('Utilisateurs exportés')

        _exporter_tarifs(filepath=filepath)
        lg.info('Tarifs exportés')

        _exporter_championnats_equipes(filepath=filepath)
        lg.info('Championnats par équipes exportés')

        _exporter_championnats_individuels(filepath=filepath)
        lg.info('Championnats individuels exportés')

        lg.info('Base de données exportée')

    except FileNotFoundError as err:
        lg.error("FileNotFoundError: %s", err)
    except NotADirectoryError as err:
        lg.error("NotADirectoryError: %s", err)
    except PermissionError as err:
        lg.error("PermissionError: %s", err)
