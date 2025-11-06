from flask import render_template

from appli.app import app
from appli.models import Article


@app.route('/')
def index():
    """Page d'accueil"""
    # noinspection PyUnresolvedReferences
    liste_articles = Article.query.filter(Article.type_article == "club").order_by(
        Article.date_publi.desc())
    article = liste_articles.first()
    return render_template('index.html', title="", article=article, articles=liste_articles)
