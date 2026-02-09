import os

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from appli.app import app, db, required_permission_lvl
from appli.forms import FormArticleAdd, FormConfirm, FormArticleUpdate
from appli.models import Article


@app.route('/club/articles/')
def articles():
    """Page des articles"""
    liste_articles = Article.query.filter(Article.type_article != "pages").all()
    return render_template('articles.html', title="Articles du club - Club",
                           articles=liste_articles)


@app.route('/club/articles/<int:id_article>/', methods=('GET', 'POST'))
def article_view(id_article):
    """Page d'un article choisi"""
    article = Article.query.get(id_article)
    ancienne_image = article.image
    form = FormArticleUpdate()
    # pylint: disable=duplicate-code
    if current_user.is_authenticated and current_user.role_au_moins("ecrivain"):
        if form.validate_on_submit():
            filename = None
            if form.image.data is not None:
                filename = form.filename()
                image = form.image.data
                image.save(os.path.join("appli", "static", "upload", filename))
                if ancienne_image  != "" and ancienne_image is not None and os.path.exists(
                        os.path.join("appli", "static", "upload", ancienne_image)):
                    os.remove(os.path.join("appli", "static", "upload", ancienne_image))
            form.update_article(article, filename)


    return render_template("article_view.html", title=article.titre, article=article, form=form,
                           contenu=article.contenu)


@app.route('/club/articles/create/', methods=('GET', 'POST'))
@required_permission_lvl("ecrivain")
def article_create():
    """Page de création d'un article"""
    form = FormArticleAdd()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            filename = None
            if form.image.data is not None:
                filename = form.filename()
                image = form.image.data
                image.save(os.path.join("appli", "static", "upload", filename))
            article = form.creation_article(filename)
            return redirect(form.next.data or url_for("article_view", id_article=article.id))
    return render_template("article_add.html", title="Ajout d'un article", form=form)


@app.route('/club/articles/<id_article>/delete/', methods=('GET', 'POST'))
@required_permission_lvl("ecrivain")
def article_delete(id_article):
    """Page de suppression d'un article choisi"""
    form = FormConfirm()
    article = Article.query.get(id_article)
    if form.validate_on_submit():
        if article.image  != "" and article.image is not None and os.path.exists(os.path.join(
                "appli", "static", "upload", article.image)):
            os.remove(os.path.join("appli", "static", "upload", article.image))
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for("articles"))
    return render_template("article_delete.html", form=form,
                           title="Suppression d'un article", article=article)
