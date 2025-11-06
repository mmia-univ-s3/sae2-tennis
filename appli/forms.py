import datetime
import os
import random
from hashlib import sha256

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import IntegerField, RadioField, BooleanField, FloatField, SelectField, StringField, \
    HiddenField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

from appli.models.article import Article
from appli.models.partenaire import Partenaire
from appli.models.utilisateur import Utilisateur
from .app import db


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
    nom = StringField('Nom du partenaire', validators=[DataRequired()])
    logo = FileField('Logo du partenaire (JPG ou PNG uniquement)', validators=[FileRequired(),
                     FileAllowed(
                         ['jpg', 'png'],
                         "Merci de n'envoyer que des fichiers JPG ou PNG.")])
    next = HiddenField()

    def confirm(self, filename):
        partenaire = Partenaire(self.nom.data, filename)
        db.session.add(partenaire)
        db.session.commit()
        return partenaire

    def filename(self):
        _, ext = os.path.splitext(self.logo.data.filename)
        filename = f'{hex(random.randrange(16 ** 48))[2:]}'
        return filename + ext


class FormReservationAdd(FlaskForm):
    intitule = StringField('Intitule de la réservation', validators=[DataRequired()])
    montant = FloatField('Montant (€)', validators=[DataRequired()])


class FormReductionAdd(FlaskForm):
    intitule = StringField('Intitulé de la réduction', validators=[DataRequired()])
    taux = StringField('Réduction', validators=[DataRequired()])
    cumulable = BooleanField('Cumulable')


class FormSouscategorieAdd(FlaskForm):
    intitule = StringField("Intitulé de la sous-catégorie", validators=[DataRequired()])


class FormCategorieAdd(FlaskForm):
    intitule = StringField("Intitulé de la catégorie", validators=[DataRequired()])
    sport = SelectField("Sport", validators=[DataRequired()],
                        choices=[("tennis", "Tennis"), ("padel", "Padel")])


class FormHistoireAdd(FlaskForm):
    annee = IntegerField("Année", validators=[DataRequired()])
    trivia = StringField("Texte", validators=[DataRequired()])


class FormArticleAdd(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired()])
    editor = StringField('Contenu')
    type_a = RadioField('Type', choices=[('club', 'Club'), ('stade', 'Stade')], default=1,
                        coerce=str)
    next = HiddenField()

    def creation_article(self):
        article = Article(self.titre.data, self.editor.data, datetime.date.today(),
                          self.type_a.data)
        db.session.add(article)
        db.session.commit()
        return article
