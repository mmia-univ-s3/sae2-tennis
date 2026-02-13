from datetime import date

from flask import render_template

from appli.app import app
from appli.models import Article, Championnat, Partenaire, Opposer, Affronter
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
    competitions = Championnat.query.filter(Championnat.date_championnat >= date.today()).all()
    parts_premium = []
    for part in Partenaire.query.order_by(Partenaire.nom).all():
        if part.important:
            parts_premium.append(part)
    les_matchs = Opposer.query.filter(Opposer.date_match >= date.today(),
                                      Opposer.mise_avant).all() + \
                 Affronter.query.filter(Affronter.date_match >= date.today(),
                                        Affronter.mise_avant).all()
    matchs = []
    for match in les_matchs:
        if isinstance(match, Opposer):
            matchs.append(("indiv", match))
        else:
            matchs.append(("equipe", match))
    matchs = sorted(matchs, key=lambda m: m[1].date_match)
    return render_template('index.html', title="", article=article,
                           articles=liste_articles, adresse=adresse.contenu, tel=tel.contenu,
                           mail=mail.contenu, reseaux=reseaux.contenu,
                           championnats_passes=championnats, championnats_futur=competitions,
                           partenaires=parts_premium, matchs=matchs)
