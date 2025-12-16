import csv
import logging as lg
from datetime import date

import click

from .app import app, db
from .models import Article, Histoire, Partenaire, Utilisateur, CategorieTarif, Tarif, \
    Reservation, Reduction, Division, ChampionnatEquipe, ChampionnatIndividuel, Equipe, \
    Participer, Affronter, Joueur, Classer


def _importer_articles(filename):
    """Permet d'importer les articles"""
    with open(filename, newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            article = Article(titre=ligne["titreArt"], contenu=ligne["contenu"],
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
                                trivia=ligne["trivia"], article=ligne["article"])
            db.session.add(histoire)
    db.session.commit()


def _importer_partenaires(filename):
    """Permet d'importer les partenaires du club"""
    with open(filename, newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            partenaire = Partenaire(nom=ligne["nomP"], logo=ligne["logo"])
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
    with open(filepath + "/categorie.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            if ligne["idCatParent"] == "":
                categorie = CategorieTarif(sport=ligne["sport"], intitule=ligne["intituleCat"])
            else:
                categorie = CategorieTarif(sport=ligne["sport"], intitule=ligne["intituleCat"],
                                           id_parent=int(ligne["idCatParent"]))
            db.session.add(categorie)

    with open(filepath + "/tarif.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            tarif = Tarif(intitule=ligne["intituleT"], id_cat=int(ligne["idCat"]))
            db.session.add(tarif)

    with open(filepath + "/reservation.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            reservation = Reservation(id_tarif=int(ligne["idT"]), montant=float(ligne["montant"]))
            db.session.add(reservation)

    with open(filepath + "/reduction.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            reduction = Reduction(id_tarif=int(ligne["idT"]), taux=ligne["taux"],
                                  cumulable=ligne["estCumulable"].strip() == "True")
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
            db.session.add(champ)

    with open(filepath + "/equipe.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            equipe = Equipe(nom=ligne["nomE"], categorie=ligne["categorieE"],
                            id_div=int(ligne["idDiv"]), rang=ligne["rangDiv"])
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
    """Permet d'importer les données relatives aux championnats par équipes"""
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
            db.session.add(champ)

    with open(filepath + "/classer.csv", newline="", encoding="utf-8") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile, delimiter=';')
        for ligne in lecture:
            classer = Classer(id_championnat=int(ligne["idCha"]), id_j=int(ligne["idJ"]),
                              rang=int(ligne["rang"]))
            db.session.add(classer)
    db.session.commit()


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
