from flask import render_template

from appli.app import app
from appli.models import Article
from appli.views.contacts import get_contacts_data


@app.route('/')
def index():
    """Page d'accueil"""
    # noinspection PyUnresolvedReferences
    liste_articles = Article.query.filter(Article.type_article == "club").order_by(
        Article.date_publi.desc())
    article = liste_articles.first()
    adresse, tel, mail, reseaux = get_contacts_data()
    return render_template('index.html', title="", article=article, articles=liste_articles,
                           adresse=adresse.contenu, tel=tel.contenu, mail=mail.contenu, reseaux=reseaux.contenu)
