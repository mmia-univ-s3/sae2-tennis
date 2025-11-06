import datetime

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from appli.app import app, db
from appli.forms import FormArticleAdd, FormConfirm, FormPageEdit
from appli.models import Article


@app.route('/club/articles/')
def articles():
    liste_articles = Article.query.filter(Article.type_article != "pages").all()
    return render_template('articles.html', title="Articles du club - Club",
                           articles=liste_articles)


@app.route('/club/articles/<int:id_article>/', methods=('GET', 'POST'))
def article_view(id_article):
    article = Article.query.get(id_article)
    form = FormPageEdit()
    # pylint: disable=duplicate-code
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    return render_template("article_view.html", title=article.titre, article=article, form=form,
                           contenu=article.contenu)


@app.route('/club/articles/create/', methods=('GET', 'POST'))
@login_required
def article_create():
    form = FormArticleAdd()
    if form.validate_on_submit():
        article = form.creation_article()
        return redirect(form.next.data or url_for("article_view", id_article=article.id))
    return render_template("article_add.html", title="Ajout d'un article", form=form)


@app.route('/club/articles/<id_article>/delete/', methods=('GET', 'POST'))
@login_required
def article_delete(id_article):
    form = FormConfirm()
    article = Article.query.get(id_article)
    if form.validate_on_submit():
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for("articles"))
    return render_template("article_delete.html", form=form, title="Suppression d'un article",
                           article=article)
