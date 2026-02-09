import datetime

from flask import render_template, redirect, url_for
from flask_login import current_user

from appli.app import app, db, required_permission_lvl
from appli.forms import FormConfirm, FormHistoireAdd, FormPageEdit
from appli.models import Article
from appli.models.histoire import Histoire


# pylint: disable=duplicate-code
@app.route('/club/histoire/', methods=('GET', 'POST'))
def histoire():
    """Page de l'histoire du site"""
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_histoire" and Article.type_article == "pages").first()
    if article is None:
        article = Article("_histoire" ,"", datetime.date.today(), "pages", "")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated and current_user.role_au_moins("editeur"):
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    dates = {}
    for texte in Histoire.query.order_by(Histoire.annee).all():
        if texte.annee not in dates:
            dates[texte.annee] = []
        dates[texte.annee].append((texte.id, texte.trivia, texte.article))
    return render_template('histoire.html', title="Histoire du club - Club",
                           contenu=article.contenu, form=form, histoire=dates)


@app.route('/club/histoire/ajout/', methods=('GET', 'POST'))
@required_permission_lvl("editeur")
def histoire_ajout():
    """Page d'ajout d'une information sur l'histoire"""
    form = FormHistoireAdd()
    articles = Article.query.filter(Article.type_article != "pages")
    choix = [(0, "")]
    for article in articles:
        choix.append((article.id, article.titre))
    form.article.choices = choix
    if form.validate_on_submit():
        information = Histoire(form.annee.data, form.trivia.data,
                               form.article.data if form.article.data != 0 else None)
        db.session.add(information)
        db.session.commit()
        return redirect(url_for("histoire"))
    return render_template("histoire_add.html", form=form, title="Ajout d'une information")


@app.route('/club/histoire/<id_h>/delete/', methods=('GET', 'POST'))
@required_permission_lvl("editeur")
def histoire_delete(id_h):
    """Page de suppression d'une information sur l'histoire"""
    form = FormConfirm()
    information = Histoire.query.get(id_h)
    if form.validate_on_submit():
        db.session.delete(information)
        db.session.commit()
        return redirect(url_for("histoire"))
    return render_template("histoire_delete.html", form=form,
                           title="Suppression d'une information", id_h=id_h)
