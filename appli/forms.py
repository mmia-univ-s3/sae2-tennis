import datetime
import os
import random
from hashlib import sha256

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import IntegerField, RadioField, BooleanField, FloatField, SelectField, StringField, \
    HiddenField, DateField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, NumberRange, Optional

from appli.models.article import Article
from appli.models.partenaire import Partenaire
from appli.models.utilisateur import Utilisateur
from .app import db
from .models import ChampionnatIndividuel


class FormConfirm(FlaskForm):
    """Formulaire de confirmation (oui/non)"""


class FormPageEdit(FlaskForm):
    """Formulaire de modification d'une page"""
    editor = StringField()


class FormLogin(FlaskForm):
    """Formulaire de connexion"""
    login = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        """
        Vérifie que les identifiants sont corrects et renvoie l'utilisateur

        Returns:
            L'utilisateur si les identifiants sont corrects, None sinon
        """
        user = Utilisateur.query.get(self.login.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        password = m.hexdigest()
        return user if password == user.mdp else None


class FormRegister(FlaskForm):
    """Formulaire de création d'un utilisateur"""
    login = StringField('Identifiant', validators=[DataRequired()])
    role = SelectField('Rôle', validators=[DataRequired()], choices=[
        ("ecrivain", "Écrivain·ice"),
        ("editeur", "Éditeur·ice"),
        ("publicateur", "Publicateur·ice"),
        ("editeur", "Administrateur·ice")
    ])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    repeat_password = PasswordField('Répétez le mot de passe', validators=[DataRequired()])
    next = HiddenField()

    def confirm(self):
        """
        Confirme la création de l'utilisateur et le renvoie.

        Returns:
            L'utilisateur créé, ou None si les identifiants ne respectent pas les contraintes
        """
        m = sha256()
        m.update(self.password.data.encode())
        user = Utilisateur(self.login.data, m.hexdigest(), self.role.data)
        if (self.password.data == self.repeat_password.data and len(
                self.password.data) >= 8 and len(self.login.data) >= 5):
            db.session.add(user)
            db.session.commit()
            return user
        return None


class FormPartenaireAdd(FlaskForm):
    """Formulaire de création d'un partenaire"""
    nom = StringField('Nom du partenaire', validators=[DataRequired()])
    logo = FileField('Logo du partenaire (JPG ou PNG uniquement)', validators=[FileRequired(),
                     FileAllowed(
                         ['jpg', 'png'],
                         "Merci de n'envoyer que des fichiers JPG ou PNG.")])
    lien = StringField('Lien vers le partenaire', validators=[DataRequired()])
    next = HiddenField()
    important = RadioField('Type', choices=[(True, 'Premium'),
                                         (False, 'Normal')],
                        coerce=str)

    def confirm(self, filename):
        """
        Confirme la création d'un partenaire et le renvoie.

        Returns:
           Partenaire:  Le partenaire créé
        """
        partenaire = Partenaire(self.nom.data, filename, self.lien.data,
                                self.important.data=='True')
        db.session.add(partenaire)
        db.session.commit()
        return partenaire

    def filename(self):
        """
        Donne un nom au logo du partenaire créé

        Returns:
            str: nom du logo
        """
        _, ext = os.path.splitext(self.logo.data.filename)
        filename = f'{hex(random.randrange(16 ** 48))[2:]}'
        return filename + ext


class FormReservationAdd(FlaskForm):
    """Formulaire d'ajout d'une réservation"""
    intitule = StringField('Intitule de la réservation', validators=[DataRequired()])
    montant = FloatField('Montant (€)', validators=[DataRequired()])


class FormReductionAdd(FlaskForm):
    """Formulaire d'ajout d'une réduction"""
    intitule = StringField('Intitulé de la réduction', validators=[DataRequired()])
    taux = StringField('Réduction', validators=[DataRequired()])
    licence = BooleanField('Applicable sur Licence ?')


class FormSouscategorieAdd(FlaskForm):
    """Formulaire d'ajout d'une sous-catégorie"""
    intitule = StringField("Intitulé de la sous-catégorie", validators=[DataRequired()])


class FormCategorieAdd(FlaskForm):
    """Formulaire d'ajout d'une catégorie"""
    intitule = StringField("Intitulé de la catégorie", validators=[DataRequired()])
    sport = SelectField("Sport", validators=[DataRequired()], choices=[])


class FormHistoireAdd(FlaskForm):
    """Formulaire d'ajout d'une date"""
    annee = IntegerField("Année", validators=[DataRequired()])
    trivia = StringField("Texte", validators=[DataRequired()])
    article = SelectField("Article",  validators=[DataRequired()], coerce=int, choices=[])


class FormArticleAdd(FlaskForm):
    """Formulaire de l'ajout d'un article"""
    titre = StringField('Titre', validators=[DataRequired()])
    image = FileField('Image (JPG ou PNG uniquement)', validators=[
                               FileAllowed(
                                   ['jpg', 'png'],
                                   "Merci de n'envoyer que des fichiers JPG ou PNG.")])
    editor = StringField('Contenu')
    type_a = RadioField('Type', choices=[('club', 'Mettre en avant'),
                                         ('stade', 'Ne pas mettre en avant')],
                        coerce=str)
    next = HiddenField()

    def filename(self):
        """
        Donne un nom au logo du partenaire créé

        Returns:
            str: nom du logo
        """
        _, ext = os.path.splitext(self.image.data.filename)
        filename = f'{hex(random.randrange(16 ** 48))[2:]}'
        return filename + ext

    def creation_article(self, filename):
        """
        Créé un article et le renvoie

        Returns:
            Article: article créé
        """
        article = Article(self.titre.data, filename, self.editor.data, datetime.date.today(),
                          self.type_a.data)
        db.session.add(article)
        db.session.commit()
        return article

class FormArticleUpdate(FlaskForm):
    """Formulaire de mise à jour d'un article"""
    image = FileField('Image (JPG ou PNG uniquement)', validators=[
        FileAllowed(
            ['jpg', 'png'],
            "Merci de n'envoyer que des fichiers JPG ou PNG.")])
    editor = StringField('Contenu')
    next = HiddenField()

    def filename(self):
        """
        Donne un nom au logo du partenaire créé

        Returns:
            str: nom du logo
        """
        _, ext = os.path.splitext(self.image.data.filename)
        filename = f'{hex(random.randrange(16 ** 48))[2:]}'
        return filename + ext

    def update_article(self, article, filename):
        """
        Met à jour un article et le renvoie

        Returns:
            Article: article créé
        """
        article.contenu = self.editor.data
        article.image = filename
        db.session.commit()
        return article

class FormInternes(FlaskForm):
    """Formulaire pour ajouter et mettre à jour des tournois internes."""
    date = DateField("Date", validators=[DataRequired()])
    titre = StringField("Nom du championnat interne", validators=[DataRequired()])
    serie = StringField("Série", validators=[DataRequired()])
    joueur1 = SelectField("Joueur 1",  validators=[DataRequired()], coerce=int, choices=[])
    points1 = IntegerField("Points du joueur 1",
                           validators=[DataRequired(), NumberRange(min=0, max=9999999999,
                                                                   message='Invalid length')])
    points2 = IntegerField("Points du joueur 2",
                           validators=[DataRequired(), NumberRange(min=0, max=9999999999,
                                                                   message='Invalid length')])
    joueur2 = SelectField("Joueur 2",  validators=[DataRequired()], coerce=int, choices=[])


    def creation_interne(self):
        """
        Créer un match en interne
        :return:
            ChampionnatIndividuel: match
            None: si les deux joueurs sont les mêmes
        """
        if self.joueur1.data != self.joueur2.data:
            match = ChampionnatIndividuel(self.date.data, self.titre.data, "Interne",
                                          self.serie.data, "Club", self.joueur1.data,
                                          self.joueur2.data, self.points1.data, self.points2.data)
            db.session.add(match)
            db.session.commit()
            return match
        return None

class FormChampionnatIndividuel(FlaskForm):
    """Formulaire de création et de mise à jour d'un championnat individuel."""
    titre = StringField('Titre', validators=[DataRequired()])
    date_championnat = DateField('Date de début', validators=[DataRequired()])
    categorie = StringField('Catégorie')
    serie = StringField('Série')
    niveau = StringField('Niveau')

class FormChampionnatEquipe(FlaskForm):
    """Formulaire de création et de mise à jour d'un championnat par équipe."""
    titre = StringField('Titre', validators=[DataRequired()])
    date_championnat = DateField('Date de début', validators=[DataRequired()])
    categorie = StringField('Catégorie')
    serie = StringField('Série')

class FormClasser(FlaskForm):
    """Formulaire de création et de mise à jour d'un classement d'un joueur."""
    joueur = SelectField("Joueur", validators=[DataRequired()], default=1, coerce=int,
                         choices=[])
    rang = StringField("Rang")

class FormParticiper(FlaskForm):
    """Formulaire de création et de mise à jour d'inscription d'une équipe."""
    equipe = SelectField("Equipe", validators=[DataRequired()], default=1, coerce=int,
                         choices=[])
    rang = StringField("Rang")
    poule = StringField("Poule", validators=[DataRequired()])

class FormAffronter(FlaskForm):
    """Formulaire de création et de mise à jour d'affrontement entre 2 équipes."""
    adversaire = StringField("Nom de l'adversaire", validators=[DataRequired()])
    date = DateField("Date du match", validators=[DataRequired()])
    resultat = RadioField("Victoire de l'équipe du club ?",
                          choices=[('V', 'Victoire'), ('D', 'Défaite'), ('N', "Nul")],
                          coerce=str, validators=[Optional()])
    score = StringField("Score")
    domicile = RadioField("Lieu du match",
                          choices=[('True', "Réception"), ('False', "Déplacement")],
                          coerce=str, validators=[DataRequired()])
