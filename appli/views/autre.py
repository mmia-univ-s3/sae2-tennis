import datetime

from flask import render_template
from flask_login import current_user

from appli.app import app, db
from appli.forms import FormPageEdit
from appli.models import Article


@app.route('/autre-sports/', methods=('GET', 'POST'))
def autre():
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_autre" and Article.type_article == "pages").first()
    if article is None:
        article = Article("_autre", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    return render_template('autre.html', title="Autres sports sur le stade",
                           contenu=article.contenu, form=form)
