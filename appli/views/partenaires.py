import os

from flask import render_template, redirect, url_for

from appli.app import app, db, required_permission_lvl
from appli.forms import FormConfirm, FormPartenaireAdd
from appli.models import Partenaire, Image


@app.route('/partenaires/')
def partenaires():
    """Page de la liste des partenaires"""
    parts_premium = []
    parts_normaux = []
    for part in Partenaire.query.order_by(Partenaire.nom).all():
        if part.important:
            parts_premium.append(part)
        else:
            parts_normaux.append(part)
    parts = [parts_premium, parts_normaux]
    return render_template('partenaires.html', title="Partenaires", partenaires=parts)


@app.route('/partenaire/<id_p>/delete/', methods=("GET", "POST",))
@required_permission_lvl("administrateur")
def partenaire_delete(id_p: int):
    """Page de suppression d'un partenaire choisi"""
    part = Partenaire.query.get(id_p)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(part)
        db.session.commit()
        if os.path.exists(os.path.join("appli", "static", "upload", part.logo.nom_fichier)):
            os.remove(os.path.join("appli", "static", "upload", part.logo.nom_fichier))
        return redirect(url_for("partenaires"))
    return render_template("partenaires_delete.html", form=form,
                           title="Suppression d'un partenaire", parte=part)


@app.route('/partenaire/ajout/', methods=("GET", "POST",))
@required_permission_lvl("administrateur")
def partenaire_create():
    """Page de création d'un partenaire"""
    form = FormPartenaireAdd()
    if form.validate_on_submit():
        filename = form.filename()
        form.confirm(filename)
        image = Image(filename, 100, f"Image pour le partenaire \"{form.nom.data}\"")
        db.session.add(image)
        db.session.commit()
        fichier_logo = form.logo.data
        fichier_logo.save(os.path.join("appli", "static", "upload", filename))
        return redirect(form.next.data or url_for("partenaires"))
    return render_template('partenaires_add.html', title="Partenaires", form=form)
