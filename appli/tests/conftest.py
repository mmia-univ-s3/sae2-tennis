# pylint: disable=missing-function-docstring

from flask import Flask
import pytest
from appli import app, db

from appli.commands import _importer_articles, _importer_championnats_equipes,\
    _importer_championnats_individuels, _importer_partenaires, _importer_tarifs,\
    _importer_trivias, _importer_users, _importer_championnats_internes

with app.app_context():
    db.drop_all()
    db.create_all()
    _importer_articles(filename="./appli/data/init/article.csv")
    _importer_trivias(filename="./appli/data/init/histoire.csv")
    _importer_partenaires(filename="./appli/data/init/partenaire.csv")
    _importer_users(filename="./appli/data/init/utilisateur.csv")
    _importer_tarifs(filepath="./appli/data/init")
    _importer_championnats_equipes(filepath="./appli/data/init")
    _importer_championnats_individuels(filepath="./appli/data/init")
    _importer_championnats_internes(filepath="./appli/data/init")

@pytest.fixture
def testapp():
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })

    yield app

# pylint: disable=redefined-outer-name
@pytest.fixture
def client(testapp):
    return testapp.test_client()

# pylint: disable=redefined-outer-name
@pytest.fixture
def runner(testapp):
    return Flask.test_cli_runner(testapp)
