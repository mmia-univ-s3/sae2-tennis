import datetime

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from appli.app import app, db
from appli.forms import FormPageEdit
from appli.models import Article


@app.route('/contacts/')
def contacts():
    """Page de contacts"""
    adresse = Article.query.filter(
        Article.titre == "_adresse" and Article.type_article == "pages").first()
    if adresse is None:
        adresse = Article("_adresse","" ,"", datetime.date.today(), "pages")
        db.session.add(adresse)
        db.session.commit()
    tel = Article.query.filter(Article.titre == "_tel" and Article.type_article == "pages").first()
    if tel is None:
        tel = Article("_tel", "" ,"", datetime.date.today(), "pages")
        db.session.add(tel)
        db.session.commit()
    mail = Article.query.filter(
        Article.titre == "_mail" and Article.type_article == "pages").first()
    if mail is None:
        mail = Article("_mail", "" ,"", datetime.date.today(), "pages")
        db.session.add(mail)
        db.session.commit()
    return render_template('contacts.html', title="Contacts", adresse=adresse.contenu,
                           tel=tel.contenu, mail=mail.contenu)


@app.route('/contacts/adresse/', methods=("GET", "POST",))
@login_required
def contacts_modif_adresse():
    """Page de modification de l'adresse"""
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_adresse" and Article.type_article == "pages").first()
    if article is None:
        article = Article("_adresse", "" ,"", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
            return redirect(url_for('contacts'))
    return render_template('contacts_modif_adresse.html',
                           title="Modification de l'adresse - Contacts", form=form,
                           contenu=article.contenu)


@app.route('/contacts/telephone/', methods=("GET", "POST",))
@login_required
def contacts_modif_tel():
    """Page de modification du numéro de téléphone"""
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_tel" and Article.type_article == "pages").first()
    if article is None:
        article = Article("_tel", "" ,"", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
            return redirect(url_for('contacts'))
    return render_template('contacts_modif_tel.html', title="Modification du téléphone - Contacts",
                           form=form, contenu=article.contenu)


@app.route('/contacts/email/', methods=("GET", "POST",))
@login_required
def contacts_modif_mail():
    """Page de modification de l'adresse mail"""
    form = FormPageEdit()
    article = Article.query.filter(
        Article.titre == "_mail" and Article.type_article == "pages").first()
    if article is None:
        article = Article("_mail", "" ,"", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
            return redirect(url_for('contacts'))
    return render_template('contacts_modif_mail.html', title="Modification de l'email - Contacts",
                           form=form, contenu=article.contenu)
