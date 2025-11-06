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
    # pylint: disable=protected-access,singleton-comparison
    list_cate_tennis = CategorieTarif.query.filter(CategorieTarif._id_parent == None,
                                                   CategorieTarif.sport == "tennis").all()
    list_cate_rese_tennis = filter(lambda x: (len(x.enfants) > 0 and len(
        x.enfants[0].tarifs.all()) > 0 and len(x.enfants[0].tarifs[0].reductions.all()) == 0) or (
                                                         x.parent is None and (
                                                             len(x.enfants) == 0 or (
                                                                 len(x.enfants) > 0 and len(
                                                             x.enfants[0].tarifs.all()) == 0))),
                                   list_cate_tennis)
    list_cate_redu_tennis = filter(
        lambda x: len(x.enfants) > 0 and len(x.enfants[0].tarifs.all()) > 0 and len(
            x.enfants[0].tarifs[0].reductions.all()) > 0, list_cate_tennis)
    # pylint: disable=protected-access,singleton-comparison
    list_cate_padel = CategorieTarif.query.filter(CategorieTarif._id_parent == None,
                                                  CategorieTarif.sport == "padel").all()
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
        categorie = CategorieTarif(categorie.sport, form.intitule.data, id_cat)
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
    """Page de suppression d'une catégorie"""
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
        tarif = Tarif(form.intitule.data, id_cat)
        db.session.add(tarif)
        db.session.commit()
        reservation = Reservation(tarif.id, form.montant.data)
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
        tarif = Tarif(form.intitule.data, id_cat)
        db.session.add(tarif)
        db.session.commit()
        reduction = Reduction(tarif.id, form.taux.data, form.cumulable.data)
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
    form = FormReservationAdd(intitule=reservation.tarif.intitule, montant=reservation.montant)
    if form.validate_on_submit():
        reservation.tarif.intitule = form.intitule.data
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
    form = FormReductionAdd(intitule=reduction.tarif.intitule, taux=reduction.taux,
                            cumulable=reduction.cumulable)
    if form.validate_on_submit():
        reduction.tarif.intitule = form.intitule.data
        reduction.taux = form.taux.data
        reduction.cumulable = form.cumulable.data
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_tarif_update_reduction.html',
                           title="Ajouter une réduction", form=form, reduction=reduction)
