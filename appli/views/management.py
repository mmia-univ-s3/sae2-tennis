import datetime

from flask import render_template
from flask_login import current_user

from appli.app import app, db
from appli.forms import FormPageEdit
from appli.models import Article


@app.route('/club/management/', methods=('GET', 'POST'))
def management():
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_management" and Article.type_article == "pages").first()
    if article is None:
        article = Article("_management", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    return render_template('management.html', title="Management du club - Club",
                           contenu=article.contenu, form=form)
