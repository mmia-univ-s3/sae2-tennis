# Form
sets = IntegerField("Sets gagnants",  validators=[DataRequired()])
joueur1 = SelectField("Joueur 1",  validators=[DataRequired()], coerce=int, choices=[])
points1 = StringField("Points du joueur 1", validators=[DataRequired()])
points2 = StringField("Points du joueur 2", validators=[DataRequired()])
joueur2 = SelectField("Joueur 2",  validators=[DataRequired()], coerce=int, choices=[])

#competitions
@app.route('/competitions/tournois-internes/')
def internes():
    """ Page de la liste des matchs en interne """
    championnats = ChampionnatInterne.query.all()
    print(championnats)
    resultat = []
    for championnat in championnats:
        for match in championnat.jouer:
            joueur1 = match.joueur1
            joueur2 = match.joueur2
            score1 = match.sets_gagnees_j1()
            score2 = match.sets_gagnees_j2()
            resultat.append((championnat, joueur1, score1, joueur2, score2))
    return render_template('interne_match.html',
                           title="Tournois internes - Competitions", matchs=resultat)

@app.route('/competitions/tournois-internes/add/', methods=("GET", "POST"))
@required_permission_lvl("publicateur")
def internes_add():
    """ Page d'ajout d'un match en interne """
    form = FormInternes()
    joueurs = Joueur.query.all()
    choix = []
    for joueur in joueurs:
        choix.append((joueur.id, joueur.prenom + " " + joueur.nom))

    form.joueur1.choices = choix
    form.joueur2.choices = choix

    if form.validate_on_submit():
        if len(form.points1.data) == len(form.points2.data) and form.joueur1 != form.joueur2:
            champ = ChampionnatInterne(form.date.data, form.titre.data)
            db.session.add(champ)
            db.session.commit()
            match = Jouer(champ.id, form.joueur1.data, form.joueur2.data, form.sets.data,
                          form.points1.data, form.points2.data)
            db.session.add(match)
            db.session.commit()
            return redirect(url_for("internes"))
        return render_template("interne_match_add.html", title="Ajout d'un match",
                               form=form, error=True)
    return render_template("interne_match_add.html", title="Ajout d'un match",
                           form=form, error=False)

# pylint: disable=protected-access
@app.route('/competitions/tournois-internes/<id_match>/update/', methods=("GET", "POST"))
@required_permission_lvl("publicateur")
def internes_update(id_match):
    """Met à jour un tournoi interne.

    Args:
        id_match (int): L'identifiant du match."""
    championnat = ChampionnatInterne.query.get(id_match)
    match = championnat.jouer.first()
    form = FormInternes(date=championnat.date_championnat, titre=championnat.titre,
                        sets=match.sets, joueur1=match.joueur1.id, joueur2=match.joueur2.id,
                        points1=match.score1, points2=match.score2)

    joueurs = Joueur.query.all()
    choix = []
    for joueur in joueurs:
        choix.append((joueur.id, joueur.prenom + " " + joueur.nom))

    form.joueur1.choices = choix
    form.joueur2.choices = choix

    if form.validate_on_submit():
        if len(form.points1.data) == len(form.points2.data) and form.joueur1 != form.joueur2:
            championnat.date_championnat = form.date.data
            championnat.titre = form.titre.data
            match.sets = form.sets.data
            match._id_j1 = form.joueur1.data
            match._id_j2 = form.joueur2.data
            match.score1 = form.points1.data
            match.score2 = form.points2.data
            db.session.commit()
            return redirect(url_for("internes"))
        return render_template("interne_match_update.html",
                               title="Modification du match", form=form, error=True,
                               id_match=id_match)
    return render_template("interne_match_update.html", title="Modification du match",
                           form=form, error=False,id_match=id_match)

@app.route('/competitions/tournois-internes/<id_match>/delete/', methods=("GET", "POST"))
@required_permission_lvl("publicateur")
def internes_delete(id_match):
    """Supprime un tournoi interne.

    Args:
        id_match (int): L'identifiant du match."""
    match = ChampionnatInterne.query.get(id_match)
    form = FormConfirm()
    if form.validate_on_submit():
        db.session.delete(match)
        db.session.commit()
        return redirect(url_for('internes'))
    return render_template("interne_match_delete.html", title="Suppression du match",
                           form=form, id_match=id_match)