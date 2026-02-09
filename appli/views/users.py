import random
from hashlib import sha256

from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, current_user

from appli.app import app, db, required_permission_lvl, get_nom_role
from appli.forms import FormConfirm, FormLogin, FormRegister
from appli.models import Utilisateur


@app.route('/connexion/', methods=('GET', 'POST'))
def connexion():
    """Page de connexion d'un administrateur"""
    form = FormLogin()
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
@required_permission_lvl("administrateur")
def utilisateurs():
    """Page de gestion des utilisateurs"""
    return render_template('utilisateurs.html', title="Gestion des utilisateurs",
                           users=Utilisateur.query.all(), get_nom_role=get_nom_role)


@app.route('/utilisateurs/create/', methods=("GET", "POST",))
@required_permission_lvl("administrateur")
def utilisateurs_create():
    """Formulaire de création d'un administrateur"""
    form = FormRegister()
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    elif form.validate_on_submit():
        user = form.confirm()
        if user:
            return redirect(form.next.data or url_for("utilisateurs"))
    return render_template("utilisateurs_add.html", form=form, title="Créer un utilisateur")


@app.route('/utilisateurs/<login>/reset/', methods=("GET", "POST",))
@required_permission_lvl("administrateur")
def utilisateurs_reset(login: str):
    """Page de réinitialisation de mot de passe d'un administrateur"""
    user = Utilisateur.query.get(login)
    form = FormConfirm()
    if form.validate_on_submit():
        mdp = ''.join(chr(random.randint(45, 122)) for _ in range(10))
        m = sha256()
        m.update(mdp.encode())
        user.mdp = m.hexdigest()
        db.session.commit()
        return render_template("utilisateurs_reset_view.html", form=form,
                               title="Réinitialisation du mot de passe", user=user, mdp=mdp)
    return render_template("utilisateurs_reset.html", form=form,
                           title="Réinitialisation du mot de passe", user=user)


@app.route('/utilisateurs/<login>/delete/', methods=("GET", "POST",))
@required_permission_lvl("administrateur")
def utilisateurs_delete(login: str):
    """Formulaire de suppression d'un administrateur"""
    if login == current_user.login:
        return redirect(url_for("utilisateurs"))
    user = Utilisateur.query.get(login)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("utilisateurs"))
    return render_template("utilisateurs_delete.html", form=form,
                           title="Supprimer un utilisateur", user=user)
