import click, logging as lg
from .app import app, db

from .models import *

def _importer_articles(filename):
    """Permet d'importer les articles"""
    import csv
    from datetime import date
    with open(filename, newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            article = Article(titre=ligne["titreArt"], contenu=ligne["contenu"],
                            date_publi=date.fromisoformat(ligne["dateArt"]),
                            type_article=ligne["typeArt"])
            db.session.add(article)
    db.session.commit()
    
def _importer_trivias(filename):
    """Permet d'importer les trivias liés à l'histoire du club"""
    import csv
    with open(filename, newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            histoire = Histoire(annee=int(ligne["annee"]), trivia=ligne["trivia"])
            db.session.add(histoire)
    db.session.commit()
    
def _importer_partenaires(filename):
    """Permet d'importer les partenaires du club"""
    import csv
    with open(filename, newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            partenaire = Partenaire(nom=ligne["nomP"], logo=ligne["logo"])
            db.session.add(partenaire)
    db.session.commit()
    
def _importer_users(filename):
    """Permet d'importer les utilisateurs"""
    import csv
    with open(filename, newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            utilisateur = Utilisateur(login=ligne["idU"], mdp=ligne["mdp"])
            db.session.add(utilisateur)
    db.session.commit()
    
def _importer_tarifs(filepath):
    """Permet d'importer les tarifs"""
    import csv
    with open(filepath+"/categorie.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            if ligne["idCatParent"] == "":
                categorie = CategorieTarif(sport=ligne["sport"], intitule=ligne["intituleCat"])
            else:
                categorie = CategorieTarif(sport=ligne["sport"], intitule=ligne["intituleCat"],
                                        id_parent=int(ligne["idCatParent"]))
            db.session.add(categorie)

    with open(filepath+"/tarif.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            tarif = Tarif(intitule=ligne["intituleT"], id_cat=int(ligne["idCat"]))
            db.session.add(tarif)

    with open(filepath+"/reservation.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            reservation = Reservation(id_tarif=int(ligne["idT"]), montant=float(ligne["montant"]))
            db.session.add(reservation)

    with open(filepath+"/reduction.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            print(ligne)
            reduction = Reduction(id_tarif=int(ligne["idT"]), taux=ligne["taux"],
                                cumulable=ligne["estCumulable"] == "True")
            db.session.add(reduction)
    db.session.commit()

def _importer_championnats_equipes(filepath):
    """Permet d'importer les données relatives aux championnats par équipes"""
    import csv
    from datetime import date
    with open(filepath+"/division.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            division = Division(intitule=ligne["intituleDiv"])
            db.session.add(division)

    with open(filepath+"/champ_equipe.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            champ = ChampionnatEquipe(date_comp=date.fromisoformat(ligne["dateCha"]),
                                    titre=ligne["titreCha"], categorie=ligne["categorieSport"],
                                    serie=ligne["serie"], id_div=int(ligne["idDiv"]))
            db.session.add(champ)

    with open(filepath+"/equipe.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            equipe = Equipe(nom=ligne["nomE"], categorie=ligne["categorieE"],
                            id_div=int(ligne["idDiv"]), rang=int(ligne["rangDiv"]))
            db.session.add(equipe)

    with open(filepath+"/participer.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            participer = Participer(id_cha=int(ligne["idCha"]), id_equipe=int(ligne["idE"]),
                                    rang=int(ligne["rang"]), poule=ligne["poule"])
            db.session.add(participer)

    with open(filepath+"/affronter.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            affronter = Affronter(id_championnat=int(ligne["idCha"]), id_equipe=int(ligne["idE"]),
                                adversaire=ligne["nomAdv"], resultat=ligne["resultat"],
                                score=ligne["score"], stade=ligne["stade"],
                                domicile=bool(ligne["estDomicile"]), date_match=date.fromisoformat(ligne["dateMatch"]))
            db.session.add(affronter)
    db.session.commit()

def _importer_championnats_individuels(filepath):
    """Permet d'importer les données relatives aux championnats par équipes"""
    import csv
    from datetime import date
    with open(filepath+"/joueur.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            joueur = Joueur(nom=ligne["nomJ"], prenom=ligne["prenomJ"], id_equipe=int(ligne["idE"]))
            db.session.add(joueur)

    with open(filepath+"/champ_indiv.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            champ = ChampionnatIndividuel(date_comp=date.fromisoformat(ligne["dateCha"]),
                                    titre=ligne["titreCha"],
                                    categorie=ligne["categorieSport"], serie=ligne["serie"],
                                        niveau=ligne["niveau"])
            db.session.add(champ)

    with open(filepath+"/classer.csv", newline="") as csvfile:
        lecture: csv.DictReader = csv.DictReader(csvfile)
        for ligne in lecture:
            classer = Classer(id_championnat=int(ligne["idCha"]), id_j=int(ligne["idJ"]),
                            rang=int(ligne["rang"]))
            db.session.add(classer)
    db.session.commit()

@app.cli.command()
@click.argument('filepath') 
def loaddb(filepath):
    '''Creates the tables and populates them with data.'''

    #  création de toutes les tables
    db.drop_all()
    db.create_all()
    try:
        # chargement de notre base
        _importer_articles(filename=filepath+"/article.csv")
        _importer_trivias(filename=filepath+"/histoire.csv")
        _importer_partenaires(filename=filepath+"/partenaire.csv")
        _importer_users(filename=filepath+"/utilisateur.csv")
        _importer_tarifs(filepath=filepath)
        _importer_championnats_equipes(filepath=filepath)
        _importer_championnats_individuels(filepath=filepath)

        lg.info('Database initialized!')
    except FileNotFoundError as err:
        lg.error("FileNotFoundError:", err)
    except NotADirectoryError as err:
        lg.error("NotADirectoryError:", err)
    except PermissionError as err:
        lg.error("PermissionError:", err)

@app.cli.command()
def syncdb():
    db.create_all()
    lg.info('Database synchronized!')


