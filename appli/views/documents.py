import datetime

from flask import render_template
from flask_login import current_user

from appli.app import app, db
from appli.forms import FormPageEdit
from appli.models import Article


@app.route('/club/documents/', methods=('GET', 'POST'))
def documents():
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_documents" and Article.type_article == "pages").first()
    if article is None:
        article = Article("_documents", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    return render_template('documents.html', title="Documents administratifs - Club",
                           contenu=article.contenu, form=form)
