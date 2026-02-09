from datetime import date

from flask import render_template

from appli.app import app
from appli.models import Article, Championnat
from appli.views.contacts import get_contacts_data  # pylint: disable=no-name-in-module


@app.route('/')
def index():
    """Page d'accueil"""
    # noinspection PyUnresolvedReferences
    liste_articles = Article.query.filter(Article.type_article == "club").order_by(
        Article.date_publi.desc())
    article = liste_articles.first()
    adresse, tel, mail, reseaux = get_contacts_data()
    championnats = Championnat.query.filter(Championnat.date_championnat <= date.today()).all()
    print(championnats)
    competitions = Championnat.query.filter(Championnat.date_championnat >= date.today()).all()
    print(competitions)

    return render_template('index.html', title="", article=article,
                           articles=liste_articles, adresse=adresse.contenu, tel=tel.contenu,
                           mail=mail.contenu, reseaux=reseaux.contenu,
                           championnats_passes=championnats, championnats_futur=competitions)
