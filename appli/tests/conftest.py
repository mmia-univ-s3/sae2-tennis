from flask import Flask
import pytest
from appli import app, db

from appli.commands import _importer_articles, _importer_championnats_equipes, _importer_championnats_individuels, _importer_partenaires, _importer_tarifs, _importer_trivias, _importer_users

with app.app_context():
    filepath = "./appli/data"
    db.drop_all()
    db.create_all()
    _importer_articles(filename=filepath + "/article.csv")
    _importer_trivias(filename=filepath + "/histoire.csv")
    _importer_partenaires(filename=filepath + "/partenaire.csv")
    _importer_users(filename=filepath + "/utilisateur.csv")
    _importer_tarifs(filepath=filepath)
    _importer_championnats_equipes(filepath=filepath)
    _importer_championnats_individuels(filepath=filepath)

@pytest.fixture
def testapp():
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })

    yield app

@pytest.fixture
def client(testapp):
    return testapp.test_client()
