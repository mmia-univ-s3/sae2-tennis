from flask import render_template, redirect, url_for
from flask_login import login_required

from appli.app import app, db
from appli.forms import FormCategorieAdd, FormConfirm, FormSouscategorieAdd, FormReductionAdd, \
    FormReservationAdd
from appli.models import CategorieTarif, Reduction, Reservation, Tarif


# noinspection PyProtectedMember,PyComparisonWithNone
@app.route('/formation/tarifications/')
def tarifications():
    """Page des tarifs"""
    list_cate_rese_tennis = filter(lambda catTarif: not catTarif.est_sous_categorie(),
                                   CategorieTarif.query.filter(CategorieTarif.type_tarif == "reservation",
                                                               CategorieTarif.sport == "tennis").all())
    list_cate_redu_tennis = filter(lambda catTarif: not catTarif.est_sous_categorie(),
                                   CategorieTarif.query.filter(CategorieTarif.type_tarif == "reduction",
                                                               CategorieTarif.sport == "tennis").all())
    list_cate_padel = filter(lambda catTarif: not catTarif.est_sous_categorie(),
                             CategorieTarif.query.filter(CategorieTarif.sport == "padel").all())
    return render_template('tarifications.html', title="Tarifications - Formation",
                           cate_rese=list_cate_rese_tennis, cate_redu=list_cate_redu_tennis,
                           cate_padel=list_cate_padel)


@app.route('/formation/tarifications/categorie/<id_cat>/souscategorie/', methods=('GET', 'POST'))
@login_required
def tarifications_souscategorie_ajout(id_cat):
    """Page d'ajout d'une sous-catégorie"""
    form = FormSouscategorieAdd()
    categorie = CategorieTarif.query.get(id_cat)
    if form.validate_on_submit():
        categorie = CategorieTarif(categorie.sport, form.intitule.data, categorie.type_tarif, id_cat)
        db.session.add(categorie)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_souscategorie_add.html',
                           title="Ajouter une sous-catégorie", id_cat=id_cat, form=form)


@app.route('/formation/tarifications/ajout/categorie/', methods=('GET', 'POST'))
@login_required
def tarifications_categorie_ajout():
    """Page d'ajout d'une catégorie"""
    form = FormCategorieAdd()
    if form.validate_on_submit():
        categorie = CategorieTarif(form.sport.data, form.intitule.data)
        db.session.add(categorie)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_categorie_add.html', title="Ajouter une catégorie",
                           form=form)


@app.route('/formation/tarifications/categorie/<id_cat>/ajout/')
@login_required
def tarifications_tarif_ajout(id_cat):
    """Page d'ajout d'un tarif"""
    return render_template('tarifications_tarif_add.html',
                           title="Ajouter un tarif dans une catégorie", id_cat=id_cat)


@app.route('/formation/tarifications/categorie/<id_cat>/delete/', methods=('GET', 'POST'))
@login_required
def tarifications_categorie_delete(id_cat):
    """Page de suppression d'une catégorie ou d'une sous-catégorie"""
    categorie = CategorieTarif.query.get(id_cat)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(categorie)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_categorie_delete.html',
                           title="Supprimer une catégorie ou sous-catégorie", id_cat=id_cat,
                           form=form, categorie=categorie)


@app.route('/formation/tarifications/tarif/<id_t>/delete/', methods=('GET', 'POST'))
@login_required
def tarifications_tarif_delete(id_t):
    """Page de suppression d'un tarif"""
    tarif = Tarif.query.get(id_t)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(tarif)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_tarif_delete.html', title="Supprimer un tarif",
                           idt=id_t, tarif=tarif, form=form)


@app.route('/formation/tarifications/categorie/<id_cat>/ajout/reservation/',
           methods=('GET', 'POST'))
@login_required
def tarifications_ajout_tarif_reservation(id_cat):
    """Page d'ajout d'une réservation"""
    form = FormReservationAdd()
    if form.validate_on_submit():
        reservation = Reservation(form.intitule.data, id_cat, form.montant.data)
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_tarif_add_reservation.html',
                           title="Ajouter une réservation", form=form, id_cat=id_cat)


@app.route('/formation/tarifications/categorie/<id_cat>/ajout/reduction/', methods=('GET', 'POST'))
@login_required
def tarifications_ajout_tarif_reduction(id_cat):
    """Page d'ajout d'une réduction"""
    form = FormReductionAdd()
    if form.validate_on_submit():
        reduction = Reduction(form.intitule.data, id_cat, form.taux.data, form.licence.data)
        db.session.add(reduction)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_tarif_add_reduction.html',
                           title="Ajouter une réduction", form=form, id_cat=id_cat)


@app.route('/formation/tarifications/tarif/<id_tarif>/update-reservation/', methods=('GET', 'POST'))
@login_required
def tarifications_reservations_update(id_tarif):
    """Page de modification d'une réservation"""
    reservation = Reservation.query.get(id_tarif)
    form = FormReservationAdd(intitule=reservation.intitule, montant=reservation.montant)
    if form.validate_on_submit():
        reservation.intitule = form.intitule.data
        reservation.montant = form.montant.data
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_tarif_update_reservation.html',
                           title="Ajouter une réduction", form=form, reservation=reservation)


@app.route('/formation/tarifications/tarif/<id_tarif>/update-reduction/', methods=('GET', 'POST'))
@login_required
def tarifications_reductions_update(id_tarif):
    """Page de modification d'une réduction"""
    reduction = Reduction.query.get(id_tarif)
    form = FormReductionAdd(obj=reduction)
    if form.validate_on_submit():
        reduction.intitule = form.intitule.data
        reduction.taux = form.taux.data
        reduction.licence = form.licence.data
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_tarif_update_reduction.html',
                           title="Ajouter une réduction", form=form, reduction=reduction)
