import os

from flask import render_template, redirect, url_for
from flask_login import current_user

from appli.app import app, db, required_permission_lvl
from appli.forms import FormArticleAdd, FormConfirm, FormArticleUpdate
from appli.models import Article


@app.route('/club/articles/')
def articles():
    """Page des articles"""
    liste_articles = Article.query.filter(Article.type_article != "pages")\
        .order_by(Article.date_publi.desc()).all()
    liste_annees = []
    for article in liste_articles:
        if article.date_publi.year not in liste_annees:
            liste_annees.append(article.date_publi.year)
    return render_template('articles.html', title="Articles du club - Club",
                           articles=liste_articles, annees=liste_annees,
                           annee=None)

@app.route('/club/articles/<int:annee>')
def articles_annee(annee):
    """Page des articles selon une année donnée

    Args:
        annee (int): Une année
    """
    les_articles = Article.query.filter(Article.type_article != "pages")\
        .order_by(Article.date_publi.desc()).all()
    liste_annees = []
    liste_articles = []
    for article in les_articles:
        if article.date_publi.year not in liste_annees:
            liste_annees.append(article.date_publi.year)
        if article.date_publi.year == annee:
            liste_articles.append(article)
    return render_template('articles.html', title="Articles du club - Club",
                           articles=liste_articles, annees=liste_annees,
                           annee=annee)


@app.route('/club/articles/<int:id_article>/', methods=('GET', 'POST'))
def article_view(id_article):
    """Page d'un article choisi"""
    article = Article.query.get(id_article)
    ancienne_image = article.image
    form = FormArticleUpdate(largeur=article.image.largeur if article.image is not None else 200 ,
                    description=article.image.description if article.image is not None else "")
    # pylint: disable=duplicate-code
    if current_user.is_authenticated and current_user.role_au_moins("ecrivain"):
        if form.validate_on_submit():
            filename = None
            if form.image.data is not None:
                filename = form.filename()
                image = form.image.data
                image.save(os.path.join("appli", "static", "upload", filename))
                if ancienne_image is not None and ancienne_image.nom_fichier != ""\
                and os.path.exists(
                        os.path.join("appli", "static", "upload", ancienne_image.nom_fichier)):
                    os.remove(os.path.join("appli", "static", "upload", ancienne_image.nom_fichier))
            form.update_article(article, filename, form.largeur.data, form.description.data)


    return render_template("article_view.html", title=article.titre, article=article, form=form,
                           contenu=article.contenu)


@app.route('/club/articles/create/', methods=('GET', 'POST'))
@required_permission_lvl("ecrivain")
def article_create():
    """Page de création d'un article"""
    form = FormArticleAdd()
    if form.validate_on_submit():
        filename = None
        if form.image.data is not None:
            filename = form.filename()
            image = form.image.data
            image.save(os.path.join("appli", "static", "upload", filename))
        article = form.creation_article(filename, form.largeur.data, form.description.data)
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


@app.route('/club/articles/<id_article>/delete/image/', methods=('GET', 'POST'))
@required_permission_lvl("ecrivain")
def article_delete_image(id_article):
    """Page de suppression d'une image d'un article"""
    form = FormConfirm()
    article = Article.query.get(id_article)
    if form.validate_on_submit():
        if article.image != "" and article.image is not None:
            db.session.delete(article.image)
            db.session.commit()
            return redirect(url_for("articles"))
    return render_template("article_delete_image.html", form=form,
                           title="Suppression d'une image d'un article", article=article)
