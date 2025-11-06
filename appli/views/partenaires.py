import os

from flask import render_template, redirect, url_for
from flask_login import login_required

from appli.app import app, db
from appli.forms import FormConfirm, FormPartenaireAdd
from appli.models import Partenaire


@app.route('/partenaires/')
def partenaires():
    parts = Partenaire.query.all()
    return render_template('partenaires.html', title="Partenaires", partenaires=parts)


@app.route('/partenaire/<id_p>/delete/', methods=("GET", "POST",))
@login_required
def partenaire_delete(id_p: int):
    part = Partenaire.query.get(id_p)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(part)
        db.session.commit()
        if os.path.exists(os.path.join("appli", "static", part.logo)):
            os.remove(os.path.join("appli", "static", part.logo))
        return redirect(url_for("partenaires"))
    return render_template("partenaires_delete.html", form=form,
                           title="Suppression d'un partenaire", parte=part)


@app.route('/partenaire/ajout/', methods=("GET", "POST",))
@login_required
def partenaire_create():
    form = FormPartenaireAdd()
    if form.validate_on_submit():
        filename = form.filename()
        form.confirm(filename)
        fichier_logo = form.logo.data
        fichier_logo.save(os.path.join("appli", "static", filename))
        return redirect(form.next.data or url_for("partenaires"))
    return render_template('partenaires_add.html', title="Partenaires", form=form)
