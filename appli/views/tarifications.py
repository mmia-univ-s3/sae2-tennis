from flask import render_template, redirect, url_for
from flask_login import login_required

from appli.app import app, db
from appli.forms import FormCategorieAdd, FormConfirm, FormSouscategorieAdd, FormReductionAdd, \
    FormReservationAdd, FormSportAdd
from appli.models import CategorieTarif, Reduction, Reservation, Tarif, Sport


# noinspection PyProtectedMember,PyComparisonWithNone
@app.route('/formation/tarifications/')
def tarifications():
    """Page des tarifs"""
    dico_categories = {}
    for sport in Sport.query.all():
        dico_categories_sport = {}
        for categorie in sorted(filter(lambda cat: not cat.est_sous_categorie(),
                                       sport.categoriesTarifs),
                                key=lambda cat: cat.ordre):
            dico_sous_categories = {}
            for sous_cat in sorted(categorie.enfants, key=lambda cat: cat.ordre):
                dico_sous_categories[sous_cat] = sorted(sous_cat.tarifs,
                                                        key=lambda tarif: tarif.ordre)
            dico_categories_sport[categorie] = {"sous_cat" : dico_sous_categories,
                                                "tarifs" : sorted(categorie.tarifs,
                                                                  key=lambda tarif: tarif.ordre)}
        dico_categories[sport] = dico_categories_sport
    return render_template('tarifications.html', title="Tarifications - Formation",
                           tarifs = dico_categories)

@app.route('/formation/tarifications/<id_tarif>/monter/')
@login_required
def tarifications_monter_tarif(id_tarif):
    tarif = Tarif.query.get(id_tarif)
    categorie = tarif.categorie
    for tar in categorie.tarifs:
        if tar.ordre == tarif.ordre - 1:
            temp = categorie.tarifs.count() + 1
            if tarif.id < tar.id:
                tarif.ordre = temp
                temp = tar.ordre
                tar.ordre += 1
                db.session.flush()
                tarif.ordre = temp
                db.session.commit()
            else:
                tar.ordre = temp
                temp = tarif.ordre
                tarif.ordre -= 1
                db.session.flush()
                tar.ordre = temp
                db.session.commit()
            break
    return redirect(url_for("tarifications"))

@app.route('/formation/tarifications/<id_tarif>/descendre/')
@login_required
def tarifications_descendre_tarif(id_tarif):
    tarif = Tarif.query.get(id_tarif)
    categorie = tarif.categorie
    for tar in categorie.tarifs:
        if tar.ordre == tarif.ordre + 1:
            temp = categorie.tarifs.count() + 1
            if tarif.id < tar.id:
                tarif.ordre = temp
                temp = tar.ordre
                tar.ordre -= 1
                db.session.flush()
                tarif.ordre = temp
                db.session.commit()
            else:
                tar.ordre = temp
                temp = tarif.ordre
                tarif.ordre += 1
                db.session.flush()
                tar.ordre = temp
                db.session.commit()
            break
    return redirect(url_for("tarifications"))

@app.route('/formation/tarifications/categorie/<id_cat>/souscategorie/monter/')
@login_required
def tarifications_monter_souscategorie(id_cat):
    souscategorie = CategorieTarif.query.get(id_cat)
    categorie = souscategorie.parent
    for cate in categorie.enfants:
        if cate.ordre == souscategorie.ordre - 1:
            temp = len(categorie.enfants) + 1
            if souscategorie.id < cate.id:
                souscategorie.ordre = temp
                temp = cate.ordre
                cate.ordre += 1
                db.session.flush()
                souscategorie.ordre = temp
                db.session.commit()
            else:
                cate.ordre = temp
                temp = souscategorie.ordre
                souscategorie.ordre -= 1
                db.session.flush()
                cate.ordre = temp
                db.session.commit()
            break
    return redirect(url_for("tarifications"))

@app.route('/formation/tarifications/categorie/<id_cat>/souscategorie/descendre/')
@login_required
def tarifications_descendre_souscategorie(id_cat):
    souscategorie = CategorieTarif.query.get(id_cat)
    categorie = souscategorie.parent
    for cate in categorie.enfants:
        if cate.ordre == souscategorie.ordre + 1:
            temp = len(categorie.enfants) + 1
            if souscategorie.id < cate.id:
                souscategorie.ordre = temp
                temp = cate.ordre
                cate.ordre -= 1
                db.session.flush()
                souscategorie.ordre = temp
                db.session.commit()
            else:
                cate.ordre = temp
                temp = souscategorie.ordre
                souscategorie.ordre += 1
                db.session.flush()
                cate.ordre = temp
                db.session.commit()
            break
    return redirect(url_for("tarifications"))

@app.route('/formation/tarifications/categorie/<id_cat>/monter/')
@login_required
def tarifications_monter_categorie(id_cat):
    categorie = CategorieTarif.query.get(id_cat)
    sport = categorie.sport
    for cate in sport.categoriesTarifs:
        if cate.ordre == categorie.ordre - 1:
            temp = sport.categoriesTarifs.count() + 1
            if categorie.id < cate.id:
                categorie.ordre = temp
                temp = cate.ordre
                cate.ordre += 1
                db.session.flush()
                categorie.ordre = temp
                db.session.commit()
            else:
                cate.ordre = temp
                temp = categorie.ordre
                categorie.ordre -= 1
                db.session.flush()
                cate.ordre = temp
                db.session.commit()
            break
    return redirect(url_for("tarifications"))

@app.route('/formation/tarifications/categorie/<id_cat>/descendre/')
@login_required
def tarifications_descendre_categorie(id_cat):
    categorie = CategorieTarif.query.get(id_cat)
    sport = categorie.sport
    for cate in sport.categoriesTarifs:
        if cate.ordre == categorie.ordre + 1:
            temp = sport.categoriesTarifs.count() + 1
            if categorie.id < cate.id:
                categorie.ordre = temp
                temp = cate.ordre
                cate.ordre -= 1
                db.session.flush()
                categorie.ordre = temp
                db.session.commit()
            else:
                cate.ordre = temp
                temp = categorie.ordre
                categorie.ordre += 1
                db.session.flush()
                cate.ordre = temp
                db.session.commit()
            break
    return redirect(url_for("tarifications"))
    
@app.route('/formation/tarifications/categorie/<id_cat>/souscategorie/', methods=('GET', 'POST'))
@login_required
def tarifications_souscategorie_ajout(id_cat):
    """Page d'ajout d'une sous-catégorie"""
    form = FormSouscategorieAdd()
    categorie = CategorieTarif.query.get(id_cat)
    if form.validate_on_submit():
        sous_categorie = CategorieTarif(len(categorie.enfants) + 1, form.intitule.data,
                                        categorie.sport.id, id_cat)
        db.session.add(sous_categorie)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_souscategorie_add.html',
                           title="Ajouter une sous-catégorie", id_cat=id_cat, form=form)


@app.route('/formation/tarifications/ajout/categorie/', methods=('GET', 'POST'))
@login_required
def tarifications_categorie_ajout():
    """Page d'ajout d'une catégorie"""
    form = FormCategorieAdd()
    liste_sports = Sport.query.all()
    form.sport.choices = [(s.id, s.nom) for s in liste_sports]
    if form.validate_on_submit():
        sport = Sport.query.get(form.sport.data)
        categorie = CategorieTarif(sport.categoriesTarifs.count() + 1, form.intitule.data, sport.id)
        db.session.add(categorie)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_categorie_add.html', title="Ajouter une catégorie",
                           form=form)
    
@app.route('/formation/tarifications/ajout/sport', methods=('GET', 'POST'))
@login_required
def tarifications_sport_ajout():
    """Page d'ajout d'un sport"""
    form = FormSportAdd()
    if form.validate_on_submit():
        nom = form.nom.data
        commentaire = form.commentaire.data
        sport = Sport(nom, commentaire)
        db.session.add(sport)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return  render_template('tarifications_sport_ajout.html', title="Ajout d'un sport", form=form)

@app.route('/formation/tarifications/<id_sport>/delete/sport', methods=('GET', 'POST'))
@login_required
def tarifications_sport_delete(id_sport):
    """Page de suppression d'un sport"""
    form = FormConfirm()
    sport = Sport.query.get(id_sport)
    if form.validate_on_submit():
        db.session.delete(sport)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template("tarifications_sport_delete.html", form=form,
                           title="Suppression d'un sport", id_sport=id_sport)

@app.route('/formation/tarifications/categorie/<id_cat>/ajout/')
@login_required
def tarifications_tarif_ajout(id_cat):
    """Page d'ajout d'un tarif"""
    categorie = CategorieTarif.query.get(id_cat)
    return render_template('tarifications_tarif_add.html',
                           title="Ajouter un tarif dans une catégorie", categorie=categorie)


@app.route('/formation/tarifications/categorie/<id_cat>/delete/', methods=('GET', 'POST'))
@login_required
def tarifications_categorie_delete(id_cat):
    """Page de suppression d'une catégorie ou d'une sous-catégorie"""
    categorie = CategorieTarif.query.get(id_cat)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(categorie)
        db.session.flush()
        if categorie.est_sous_categorie():
            parent = categorie.parent
            for enfant in sorted(filter(lambda c: c.ordre > categorie.ordre, parent.enfants),
                                 key=lambda c: c.ordre):
                enfant.ordre -= 1
        else:
            sport = categorie.sport
            for cat in sorted(filter(lambda c: c.ordre > categorie.ordre\
                                      and not c.est_sous_categorie(),
                                     sport.categoriesTarifs),
                              key=lambda c: c.ordre):
                cat.ordre -= 1
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
        categorie = tarif.categorie
        db.session.delete(tarif)
        db.session.flush()
        for autre_tarif in sorted(filter(lambda t: t.ordre > tarif.ordre, categorie.tarifs),
                                  key=lambda t: t.ordre):
            autre_tarif.ordre -= 1
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
    categorie = CategorieTarif.query.get(id_cat)
    if form.validate_on_submit():
        reservation = Reservation(categorie.tarifs.count() + 1, form.intitule.data, id_cat,
                                  form.montant.data)
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
    categorie = CategorieTarif.query.get(id_cat)
    if form.validate_on_submit():
        reduction = Reduction(categorie.tarifs.count() + 1, form.intitule.data, id_cat,
                              form.taux.data, form.licence.data)
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
