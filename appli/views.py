from hashlib import sha256
import random
import datetime
import os
from flask import render_template, redirect, url_for, request
from flask_login import login_required, logout_user, login_user, current_user

from appli.forms import ArticleAjoutForm, ArticleForm, CategorieForm, ConfirmForm, HistoireForm, \
    LoginForm, PartenairesCreateForm, PageForm, RegisterForm, SousCategorieForm, \
    TarifFormReduction, TarifFormReservation
from appli.models import CategorieTarif, Partenaire, Article, Utilisateur, \
    Reduction, Reservation, Tarif
from appli.models.histoire import Histoire
from .app import app, db

@app.route('/')
def index():
    liste_articles = Article.query.filter(Article.type_article == "club") \
                                  .order_by(Article.date_publi.desc())
    article = liste_articles.first()
    return render_template('index.html', title="", article=article, articles=liste_articles)

@app.route('/club/')
def club():
    return redirect(url_for('histoire'), 301)

@app.route('/club/histoire/', methods=('GET', 'POST'))
def histoire():
    form = PageForm()
    article = Article.query.filter(Article.titre == "_histoire" and
                                   Article.type_article == "pages").first()
    if article is None:
        article = Article("_histoire", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    dates = {}
    for texte in Histoire.query.order_by(Histoire.annee).all():
        if texte.annee not in dates:
            dates[texte.annee] = []
        dates[texte.annee].append((texte.id, texte.trivia))
    return render_template('histoire.html', title="Histoire du club - Club",
                           contenu=article.contenu, form=form, histoire=dates)

@app.route('/club/histoire/<id_h>/delete/', methods=('GET', 'POST'))
@login_required
def histoire_delete(id_h):
    form = ConfirmForm()
    date = Histoire.query.get(id_h)
    if form.validate_on_submit():
        db.session.delete(date)
        db.session.commit()
        return redirect(url_for("histoire"))
    return render_template("histoire_delete_date.html", form=form,
                           title="Suppression d'une date", id_h=id_h)

@app.route('/club/histoire/ajout/', methods=('GET', 'POST'))
@login_required
def histoire_ajout():
    form = HistoireForm()
    if form.validate_on_submit():
        date = Histoire(form.annee.data, form.trivia.data)
        db.session.add(date)
        db.session.commit()
        return redirect(url_for("histoire"))
    return render_template("histoire_ajout_date.html", form=form,
                           title="Ajout d'une date")

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
    liste_articles = Article.query.filter(Article.type_article != "pages").all()
    return render_template('articles.html', title="Articles du club - Club",
                           articles = liste_articles)

@app.route('/club/articles/<int:id_article>/', methods=('GET', 'POST'))
def article_view(id_article):
    article = Article.query.get(id_article)
    form = ArticleForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    return render_template("article_view.html", title=article.titre, article=article,
                           form=form, contenu=article.contenu)

@app.route('/club/articles/create/', methods=('GET', 'POST'))
@login_required
def article_create():
    form = ArticleAjoutForm()
    if form.validate_on_submit():
        article = form.creation_article()
        return redirect(form.next.data or url_for("article_view", id_article=article.id))
    return render_template("article_create.html", title="Ajout d'un article", form=form)

@app.route('/club/articles/<id_article>/delete/', methods=('GET', 'POST'))
@login_required
def article_delete(id_article):
    form = ConfirmForm()
    article = Article.query.get(id_article)
    if form.validate_on_submit():
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for("articles"))
    return render_template("article_delete.html", form=form,
                           title="Suppression d'un article", article=article)

@app.route('/club/documents/', methods=('GET', 'POST'))
def documents():
    form = PageForm()
    article = Article.query.filter(Article.titre == "_documents" and
                                   Article.type_article == "pages").first()
    if article is None:
        article = Article("_documents", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
    return render_template('documents.html', title="Documents administratifs - Club",
                           contenu=article.contenu, form=form)

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
    # pylint: disable=protected-access,singleton-comparison
    list_cate_tennis = CategorieTarif.query.filter(CategorieTarif._id_parent == None,
                                                   CategorieTarif.sport == "tennis").all()
    list_cate_rese_tennis = filter(lambda x: (len(x.enfants) > 0 and \
                            len(x.enfants[0].tarifs.all()) > 0 and \
                            len(x.enfants[0].tarifs[0].reductions.all()) == 0) or \
                            (x.parent is None and \
                            (len(x.enfants) == 0 or \
                            (len(x.enfants) > 0 and \
                            len(x.enfants[0].tarifs.all()) == 0))), list_cate_tennis)
    list_cate_redu_tennis = filter(lambda x: len(x.enfants) > 0 and \
                            len(x.enfants[0].tarifs.all()) > 0 and \
                            len(x.enfants[0].tarifs[0].reductions.all()) > 0, list_cate_tennis)
    # pylint: disable=protected-access,singleton-comparison
    list_cate_padel = CategorieTarif.query.filter(CategorieTarif._id_parent == None,
                                                  CategorieTarif.sport == "padel").all()
    return render_template('tarifications.html', title="Tarifications - Formation",
                           cate_rese=list_cate_rese_tennis, cate_redu=list_cate_redu_tennis,
                           cate_padel=list_cate_padel)

@app.route('/formation/tarifications/categorie/<id_cat>/souscategorie/', methods=('GET', 'POST'))
@login_required
def tarifications_souscategorie_ajout(id_cat):
    form = SousCategorieForm()
    categorie = CategorieTarif.query.get(id_cat)
    if form.validate_on_submit():
        categorie = CategorieTarif(categorie.sport, form.intituleCat.data, id_cat)
        db.session.add(categorie)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_ajout_sous_categorie.html',
                           title="Ajouter une sous-catégorie", id_cat=id_cat, form=form)

@app.route('/formation/tarifications/ajout/categorie/', methods=('GET', 'POST'))
@login_required
def tarifications_categorie_ajout():
    form = CategorieForm()
    if form.validate_on_submit():
        categorie = CategorieTarif(form.sport.data, form.intituleCat.data)
        db.session.add(categorie)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_ajout_categorie.html',
                           title="Ajouter une catégorie", form=form)

@app.route('/formation/tarifications/categorie/<id_cat>/ajout/')
@login_required
def tarifications_tarif_ajout(id_cat):
    return render_template('tarifications_ajout_intitule.html',
                           title="Ajouter un tarif dans une catégorie", id_cat=id_cat)

@app.route('/formation/tarifications/categorie/<id_cat>/delete/', methods=('GET', 'POST'))
@login_required
def tarifications_categorie_delete(id_cat):
    categorie = CategorieTarif.query.get(id_cat)
    form = ConfirmForm()
    if form.validate_on_submit():
        db.session.delete(categorie)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_delete_categorie.html',
                           title="Supprimer une catégorie ou sous-catégorie",
                           id_cate=id_cat, form=form, categorie=categorie)

@app.route('/formation/tarifications/tarif/<id_t>/delete/', methods=('GET', 'POST'))
@login_required
def tarifications_tarif_delete(id_t):
    tarif = Tarif.query.get(id_t)
    form = ConfirmForm()
    if form.validate_on_submit():
        db.session.delete(tarif)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_delete_intitule.html',
                           title="Supprimer un tarif", idt=id_t, tarif=tarif, form=form)

@app.route('/formation/tarifications/categorie/<id_cat>/ajout/reservation/',
           methods=('GET', 'POST'))
@login_required
def tarifications_ajout_tarif_reservation(id_cat):
    form = TarifFormReservation()
    if form.validate_on_submit():
        tarif = Tarif(form.intituleT.data, id_cat)
        db.session.add(tarif)
        db.session.commit()
        reservation = Reservation(tarif.id, form.montant.data)
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_ajout_tarif_reservation.html',
                           title="Ajouter une réservation", form=form, id_cat=id_cat)

@app.route('/formation/tarifications/categorie/<id_cat>/ajout/reduction/', methods=('GET', 'POST'))
@login_required
def tarifications_ajout_tarif_reduction(id_cat):
    form = TarifFormReduction()
    if form.validate_on_submit():
        tarif = Tarif(form.intituleT.data, id_cat)
        db.session.add(tarif)
        db.session.commit()
        reduction = Reduction(tarif.id, form.taux.data, form.estCumulable.data)
        db.session.add(reduction)
        db.session.commit()
        return redirect(url_for("tarifications"))
    return render_template('tarifications_ajout_tarif_reduction.html',
                           title="Ajouter une réduction", form=form, id_cat=id_cat)

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
    parts = Partenaire.query.all()
    return render_template('partenaires.html', title="Partenaires", partenaires = parts)

@app.route('/partenaire/<id_p>/delete/', methods=("GET", "POST",))
@login_required
def partenaire_delete(id_p: int):
    part = Partenaire.query.get(id_p)
    form = ConfirmForm()
    if form.validate_on_submit():
        db.session.delete(part)
        db.session.commit()
        if os.path.exists(os.path.join("appli", "static", part.logo)):
            os.remove(os.path.join("appli", "static", part.logo))
        return redirect(url_for("partenaires"))
    return render_template("partenaires_delete.html", form=form,
                           title="Suppression d'un partenaire", parte = part)

@app.route('/partenaire/ajout/', methods=("GET", "POST",))
@login_required
def partenaire_create():
    form = PartenairesCreateForm()
    if form.validate_on_submit():
        filename = form.filename()
        form.confirm(filename)
        photo = form.logo.data
        photo.save(os.path.join("appli", "static", filename))
        return redirect(form.next.data or url_for("partenaires"))
    return render_template('partenaires_ajout.html', title="Partenaires", form=form)

@app.route('/contacts/')
def contacts():
    adresse = Article.query.filter(Article.titre == "_adresse" and
                                   Article.type_article == "pages").first()
    if adresse is None:
        adresse = Article("_adresse", "", datetime.date.today(), "pages")
        db.session.add(adresse)
        db.session.commit()
    tel = Article.query.filter(Article.titre == "_tel" and
                                   Article.type_article == "pages").first()
    if tel is None:
        tel = Article("_tel", "", datetime.date.today(), "pages")
        db.session.add(tel)
        db.session.commit()
    mail = Article.query.filter(Article.titre == "_mail" and
                                   Article.type_article == "pages").first()
    if mail is None:
        mail = Article("_mail", "", datetime.date.today(), "pages")
        db.session.add(mail)
        db.session.commit()
    return render_template('contacts.html', title="Contacts", adresse=adresse.contenu, tel=tel.contenu, mail=mail.contenu)

@app.route('/contacts/modif_adresse/', methods=("GET", "POST",))
@login_required
def contacts_modif_adresse():
    form = PageForm()
    article = Article.query.filter(Article.titre == "_adresse" and
                                   Article.type_article == "pages").first()
    if article is None:
        article = Article("_adresse", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
            return redirect(url_for('contacts'))
    return render_template('contacts_modif_adresse.html', title="Contacts",
                           form=form, contenu=article.contenu)
    
@app.route('/contacts/modif_tel/', methods=("GET", "POST",))
@login_required
def contacts_modif_tel():
    form = PageForm()
    article = Article.query.filter(Article.titre == "_tel" and
                                   Article.type_article == "pages").first()
    if article is None:
        article = Article("_tel", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
            return redirect(url_for('contacts'))
    return render_template('contacts_modif_tel.html', title="Contacts",
                           form=form, contenu=article.contenu)
    
@app.route('/contacts/modif_mail/', methods=("GET", "POST",))
@login_required
def contacts_modif_mail():
    form = PageForm()
    article = Article.query.filter(Article.titre == "_mail" and
                                   Article.type_article == "pages").first()
    if article is None:
        article = Article("_mail", "", datetime.date.today(), "pages")
        db.session.add(article)
        db.session.commit()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            article.contenu = form.editor.data
            article.date = datetime.date.today()
            db.session.commit()
            return redirect(url_for('contacts'))
    return render_template('contacts_modif_mail.html', title="Contacts",
                           form=form, contenu=article.contenu)

@app.route('/autre-sports/', methods=('GET', 'POST'))
def autre():
    form = PageForm()
    article = Article.query.filter(Article.titre == "_autre" and
                                   Article.type_article == "pages").first()
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
def e405(_):
    return render_template('error.html', error_code=405,
                           error_message="Cette méthode n'est pas autorisée.")

if __name__ == "__main__":
    app.run()
