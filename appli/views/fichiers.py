import os.path

from flask import render_template, redirect, url_for

from appli.app import app, required_permission_lvl, db
from appli.forms import FormConfirm, FormFichierAdd, FormFichierUpdate
from appli.models import Image

@app.route('/fichiers/', methods=('GET', 'POST'))
@required_permission_lvl("ecrivain")
def fichiers_list():
    """Page de gestion des fichiers"""
    fichiers = Image.query.all()
    tailles_fichiers = {}

    for fichier in fichiers:
        tailles_fichiers[fichier.nom_fichier] = None
        nom = os.path.join("appli", "static", "upload", fichier.nom_fichier)
        # noinspection PyBroadException
        try:
            if os.path.exists(nom):
                tailles_fichiers[fichier.nom_fichier] = os.path.getsize(nom)
        except Exception:
            pass

    return render_template('fichiers.html', title="Gestion des fichiers",
                           fichiers=fichiers, tailles=tailles_fichiers,
                           get_pretty_size=get_pretty_size)

@app.route('/fichiers/create/', methods=('GET', 'POST'))
@required_permission_lvl("ecrivain")
def fichiers_create():
    """Page de mise en ligne d'un nouveau fichier"""
    form = FormFichierAdd()
    if form.validate_on_submit():
        filename = form.filename()
        image = form.image.data
        image.save(os.path.join("appli", "static", "upload", filename))
        fichier = form.creation_fichier(filename)
        return redirect(url_for("fichiers_update", nom_fichier=fichier.nom_fichier))
    return render_template("fichiers_create.html", title="Ajout d'un fichier", form=form)

@app.route('/fichiers/<nom_fichier>/', methods=('GET', 'POST'))
@required_permission_lvl("ecrivain")
def fichiers_update(nom_fichier):
    """Page de mise à jour d'un fichier"""
    fichier = Image.query.get(nom_fichier)
    form = FormFichierUpdate(largeur=fichier.largeur if fichier is not None else 200 ,
                             description=fichier.description if fichier is not None else "")
    # pylint: disable=duplicate-code
    if form.validate_on_submit():
        form.update_fichier(fichier, form.largeur.data, form.description.data)
        return redirect(url_for("fichiers_list"))

    return render_template("fichiers_update.html", title=fichier.nom_fichier,
                           fichier=fichier, form=form)

@app.route('/fichiers/<nom_fichier>/delete/', methods=('GET', 'POST'))
@required_permission_lvl("ecrivain")
def fichiers_delete(nom_fichier):
    """Formulaire de suppression d'un fichier"""
    fichier = Image.query.get(nom_fichier)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(fichier)
        db.session.commit()
        if os.path.exists(os.path.join("appli", "static", "upload", fichier.nom_fichier)):
            os.remove(os.path.join("appli", "static", "upload", fichier.nom_fichier))
        return redirect(url_for("fichiers_list"))
    return render_template("fichiers_delete.html", form=form,
                           title="Supprimer un fichier", fichier=fichier)

def get_pretty_size(size):
    if size > 1024**2:
        return f"{round(size / 1024**2, 2)} Mio"
    elif size > 1024:
        return f"{round(size / 1024, 1)} Kio"
    else:
        return f"{size} octets"