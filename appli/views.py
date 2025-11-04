from hashlib import sha256
import random
import datetime

from flask import render_template, redirect, url_for, request
from flask_login import logout_user, login_user, login_required, current_user

from appli.forms import LoginForm, PageForm, RegisterForm, ConfirmForm
from appli.models import Article, Utilisateur
from .app import app, db

@app.route('/')
def index():
    return render_template('index.html', title="")

@app.route('/club/')
def club():
    return redirect(url_for('histoire'), 301)

@app.route('/club/histoire/')
def histoire():
    return render_template('histoire.html', title="Histoire et présentation - Club")

@app.route('/club/management/', methods=('GET', 'POST'))
def management():
    form = PageForm()
    article = Article.query.filter(Article.titre == "_management" and
                                   Article.type_article == "pages").first()
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

@app.route('/club/articles/')
def articles():
    return render_template('articles.html', title="Articles du club - Club")

@app.route('/club/documents/')
def documents():
    return render_template('documents.html', title="Documents administratifs - Club")

@app.route('/competitions/')
def competitions():
    return redirect(url_for('calendrier'), 301)

@app.route('/competitions/calendrier/')
def calendrier():
    return render_template('calendrier.html', title="Calendrier et résultats - Compétitions")

@app.route('/competitions/palmares/')
def palmares():
    return render_template('palmares.html', title="Palmarès - Competitions")

@app.route('/competitions/tournois/')
def tournois():
    return render_template('tournois.html', title="Tournois - Competitions")

@app.route('/competitions/tournois-internes/')
def internes():
    return render_template('internes.html', title="Tournois internes - Competitions")

@app.route('/formation/')
def formation():
    return redirect(url_for('tarifications'), 301)

@app.route('/formation/tarifications/')
def tarifications():
    return render_template('tarifications.html', title="Tarifications - Formation")

@app.route('/formation/ecole-de-tennis/', methods=('GET', 'POST'))
def ecole():
    form = PageForm()
    article = Article.query.filter(Article.titre == "_ecole" and
                                   Article.type_article == "pages").first()
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

@app.route('/partenaires/')
def partenaires():
    return render_template('partenaires.html', title="Partenaires")

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html', title="Contacts")

@app.route('/autre-sports/')
def autre():
    return render_template('autre.html', title="Autres sports sur le stade")

@app.route('/connexion/', methods=('GET', 'POST'))
def connexion():
    form = LoginForm()
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    elif form.validate_on_submit():
        user = form.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(form.next.data or url_for("index", name=user.login))
        return render_template("connexion.html", form=form, title="Se connecter", error=True)
    return render_template("connexion.html", form=form, title="Se connecter", error=False)

@app.route('/utilisateurs/')
@login_required
def utilisateurs():
    return render_template('utilisateurs.html', title="Gestion des utilisateurs",
                           users=Utilisateur.query.all())

@app.route('/utilisateurs/create/', methods=("GET", "POST",))
@login_required
def utilisateurs_create():
    form = RegisterForm()
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    elif form.validate_on_submit():
        user = form.confirm()
        if user:
            return redirect(form.next.data or url_for("utilisateurs"))
    return render_template("utilisateurs_create.html", form=form, title="Créer un utilisateur")

@app.route('/utilisateurs/<login>/reset/', methods=("GET", "POST",))
@login_required
def utilisateurs_reset(login: str):
    user = Utilisateur.query.get(login)
    form = ConfirmForm()
    if form.validate_on_submit():
        mdp = ''.join(chr(random.randint(45, 122)) for _ in range(10))
        m = sha256()
        m.update(mdp.encode())
        user.mdp = m.hexdigest()
        db.session.commit()
        return render_template("utilisateurs_reset.html", form=form,
                               title="Réinitialisation du mot de passe", user=user, mdp=mdp)
    return render_template("utilisateurs_reset_confirm.html", form=form,
                           title="Réinitialisation du mot de passe", user=user)


@app.route('/utilisateurs/<login>/delete/', methods=("GET", "POST",))
@login_required
def utilisateurs_delete(login: str):
    if login == current_user.login:
        return redirect(url_for("utilisateurs"))
    user = Utilisateur.query.get(login)
    form = ConfirmForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("utilisateurs"))
    return render_template("utilisateurs_delete_confirm.html",
                           form=form, title="Supprimer un utilisateur", user=user)

@app.route('/deconnexion/')
def deconnexion():
    logout_user()
    return redirect(url_for("index"))

@app.errorhandler(404)
def e404(_):
    return render_template('error.html', error_code=404, error_message="La page est introuvable.")

@app.errorhandler(500)
def e500(_):
    return render_template('error.html', error_code=500, error_message="Une erreur s'est produite.")

@app.errorhandler(405)
def e428(_):
    return render_template('error.html', error_code=405,
                           error_message="Cette méthode n'est pas autorisée.")

if __name__ == "__main__":
    app.run()
