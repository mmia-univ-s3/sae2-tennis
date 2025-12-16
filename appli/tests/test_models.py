# pylint: disable=missing-function-docstring

import datetime
from appli.models.article import Article
from appli.models.categorie_tarif import CategorieTarif
from appli.models.championnat import ChampionnatEquipe, ChampionnatIndividuel
from appli.models.classer import Classer
from appli.models.division import Division
from appli.models.equipe import Equipe
from appli.models.histoire import Histoire
from appli.models.joueur import Joueur
from appli.models.partenaire import Partenaire
from appli.models.participer import Participer
from appli.models.tarif import Tarif
from appli.models.utilisateur import Utilisateur

def test_models_utilisateur():
    var = Utilisateur("login", "password")
    assert str(var) == "<Utilisateur(login) password>"

def test_models_article():
    var = Article("titre", "contenu", datetime.date(1969, 1, 20), "type")
    assert str(var) == repr(var) == "<Article(None) titre>"

def test_models_championnat_individuel():
    var = ChampionnatIndividuel(datetime.date(1969, 1, 20), "titre", "categorie", "serie",
                                "niveau", None, None, None, None)
    assert str(var) == repr(var) == "<ChampionnatIndividuel(None) titre>"

def test_models_championnat_equipe():
    var = ChampionnatEquipe(datetime.date(1969, 1, 20), "titre", "categorie", "serie")
    assert str(var) == repr(var) == "<ChampionnatEquipe(None) titre>"

def test_models_equipe():
    var = Equipe("nom", "categorie", 1, 2)
    assert str(var) == repr(var) == "<Equipe(None) nom>"

def test_models_participer():
    var = Participer(1, 2, 3, 4)
    assert str(var) == repr(var) == "<Participer(1, 2) 4 3>"

def test_models_categorie_tarif():
    var = CategorieTarif("sport", "intitule", 5)
    assert str(var) == repr(var) == "<CategorieTarif(None) intitule>"

def test_models_classer():
    var = Classer(1, 1, 1)
    assert str(var) == repr(var) == "<Classer(1, 1) 1>"

def test_models_division():
    var = Division("intitule")
    assert str(var) == repr(var) == "<Division(None) intitule>"

def test_models_histoire():
    var = Histoire(2020, "trivia")
    assert str(var) == repr(var) == "<Histoire(None) 2020>"

def test_models_joueur():
    var = Joueur("nom", "prenom", 1)
    assert str(var) == repr(var) == "<Joueur(None) nom prenom>"

def test_models_partenaires():
    var = Partenaire("nom", "logo", "https://example.com")
    assert str(var) == repr(var) == "<Partenaire(None) nom>"

def test_models_tarif():
    var = Tarif("intitule", 1)
    assert str(var) == repr(var) == "<Tarif(None) intitule>"
