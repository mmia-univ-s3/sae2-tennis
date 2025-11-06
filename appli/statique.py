import datetime

from flask import render_template
from flask_login import current_user

from appli.app import db
from appli.forms import FormPageEdit
from appli.models import Article

# pylint: disable=duplicate-code
def page_statique(id_p, html, titre):
    """Code de base pour une page statique"""
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_" + id_p and Article.type_article == "pages").first()
    if article is None:
        article = Article("_" + id_p, "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    return render_template(html, title=titre, contenu=article.contenu, form=form)
