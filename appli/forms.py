import datetime
import os
import random
from hashlib import sha256

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import IntegerField, RadioField, BooleanField, FloatField, SelectField, StringField, \
    HiddenField, DateField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

from appli.models.article import Article
from appli.models.partenaire import Partenaire
from appli.models.utilisateur import Utilisateur
from .app import db


class FormConfirm(FlaskForm):
    pass


class FormPageEdit(FlaskForm):
    editor = StringField()


class FormLogin(FlaskForm):
    login = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        user = Utilisateur.query.get(self.login.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        password = m.hexdigest()
        return user if password == user.mdp else None


class FormRegister(FlaskForm):
    login = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    repeat_password = PasswordField('Répétez le mot de passe', validators=[DataRequired()])
    next = HiddenField()

    def confirm(self):
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
    type_a = RadioField('Type', choices=[('club', 'Club'), ('stade', 'Stade')],
                        coerce=str)
    next = HiddenField()

    def creation_article(self):
        article = Article(self.titre.data, self.editor.data, datetime.date.today(),
                          self.type_a.data)
        db.session.add(article)
        db.session.commit()
        return article

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
