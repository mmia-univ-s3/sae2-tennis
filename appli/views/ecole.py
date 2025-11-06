import datetime

from flask import render_template
from flask_login import current_user

from appli.app import app, db
from appli.forms import FormPageEdit
from appli.models import Article


@app.route('/formation/ecole-de-tennis/', methods=('GET', 'POST'))
def ecole():
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_ecole" and Article.type_article == "pages").first()
    if article is None:
        article = Article("_ecole", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    return render_template('ecole.html', title="École de Tennis - Formation",
                           contenu=article.contenu, form=form)
