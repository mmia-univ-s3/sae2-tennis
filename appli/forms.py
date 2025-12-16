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
        user = Utilisateur(self.login.data, m.hexdigest())
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
    next = HiddenField()

    def confirm(self, filename):
        """
        Confirme la création d'un partenaire et le renvoie.

        Returns:
           Partenaire:  Le partenaire créé
        """
        partenaire = Partenaire(self.nom.data, filename)
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
    cumulable = BooleanField('Cumulable')


class FormSouscategorieAdd(FlaskForm):
    """Formulaire d'ajout d'une sous-catégorie"""
    intitule = StringField("Intitulé de la sous-catégorie", validators=[DataRequired()])


class FormCategorieAdd(FlaskForm):
    """Formulaire d'ajout d'une catégorie"""
    intitule = StringField("Intitulé de la catégorie", validators=[DataRequired()])
    sport = SelectField("Sport", validators=[DataRequired()],
                        choices=[("tennis", "Tennis"), ("padel", "Padel")])


class FormHistoireAdd(FlaskForm):
    """Formulaire d'ajout d'une date"""
    annee = IntegerField("Année", validators=[DataRequired()])
    trivia = StringField("Texte", validators=[DataRequired()])


class FormArticleAdd(FlaskForm):
    """Formulaire de l'ajout d'un article"""
    titre = StringField('Titre', validators=[DataRequired()])
    editor = StringField('Contenu')
    type_a = RadioField('Type', choices=[('club', 'Mettre en avant'), ('stade', 'Ne pas mettre en avant')],
                        coerce=str)
    next = HiddenField()

    def creation_article(self):
        """
        Créé un article et le renvoie

        Returns:
            Article: article créé
        """
        article = Article(self.titre.data, self.editor.data, datetime.date.today(),
                          self.type_a.data)
        db.session.add(article)
        db.session.commit()
        return article

class FormInternes(FlaskForm):
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
        if self.joueur1.data != self.joueur2.data:
            match = ChampionnatIndividuel(self.date.data, self.titre.data, "Interne",
                                          self.serie.data, "Club", self.joueur1.data,
                                          self.joueur2.data, self.points1.data, self.points2.data)
            db.session.add(match)
            db.session.commit()
            return match
        return None

class FormChampionnatIndividuel(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired()])
    date_championnat = DateField('Date de début', validators=[DataRequired()])
    categorie = StringField('Catégorie')
    serie = StringField('Série')
    niveau = StringField('Niveau')

class FormChampionnatEquipe(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired()])
    date_championnat = DateField('Date de début', validators=[DataRequired()])
    categorie = StringField('Catégorie')
    serie = StringField('Série')

class FormClasser(FlaskForm):
    joueur = SelectField("Joueur", validators=[DataRequired()], default=1, coerce=int,
                         choices=[])
    rang = StringField("Rang")

class FormParticiper(FlaskForm):
    equipe = SelectField("Equipe", validators=[DataRequired()], default=1, coerce=int,
                         choices=[])
    rang = StringField("Rang")
    poule = StringField("Poule", validators=[DataRequired()])

class FormAffronter(FlaskForm):
    adversaire = StringField("Nom de l'adversaire", validators=[DataRequired()])
    date = DateField("Date du match", validators=[DataRequired()])
    resultat = RadioField("Victoire de l'équipe du club ?",
                          choices=[('V', 'Victoire'), ('D', 'Défaire'), ('N', "Nul")],
                          coerce=str, validators=[Optional()])
    score = StringField("Score")
    domicile = RadioField("Lieu du match",
                          choices=[('True', "Réception"), ('False', "Déplacement")],
                          coerce=str, validators=[DataRequired()])
