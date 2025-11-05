from hashlib import sha256
import os
import random

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import BooleanField, FloatField, IntegerField, SelectField, StringField, HiddenField
# from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

from appli.models.partenaire import Partenaire
from appli.models.utilisateur import Utilisateur

from .app import db

# from wtforms.validators import DataRequired
# from hashlib import sha256

# class FormAuteur(FlaskForm):
#     idA = HiddenField()
#     nom = StringField('Nom', validators=[DataRequired()])

class LoginForm(FlaskForm):
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

class ConfirmForm(FlaskForm):
    pass

class PartenairesCreateForm(FlaskForm):
    nom = StringField('Nom du partenaire', validators=[DataRequired()])
    logo = FileField('Logo du partenaire (JPG ou PNG uniquement)',
                     validators=[FileRequired(), FileAllowed(['jpg', 'png'],
                                 "Merci de n'envoyer que des fichiers JPG ou PNG.")])
    next = HiddenField()

    def confirm(self, filename):
        partenaire = Partenaire(self.nom.data, filename)
        db.session.add(partenaire)
        db.session.commit()
        return partenaire

    def filename(self):
        _, ext = os.path.splitext(self.logo.data.filename)
        filename = f'{hex(random.randrange(16**48))[2:]}'
        return filename + ext
    
class TarifFormReservation(FlaskForm):
    intituleT = StringField('Intitule du tarif', validators=[DataRequired()])
    montant = FloatField('Montant du tarif', validators=[DataRequired()])
    
class TarifFormReduction(FlaskForm):
    intituleT = StringField('Intitulé du tarif', validators=[DataRequired()])
    taux = StringField('La réduction', validators=[DataRequired()])
    estCumulable = BooleanField('Cumulable')
    
class SousCategorieForm(FlaskForm):
    intituleCat = StringField("L'intitulé de la catégorie", validators=[DataRequired()])

class PageForm(FlaskForm):
    editor = StringField()

class RegisterForm(FlaskForm):
    login = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    repeat_password = PasswordField('Répétez le mot de passe', validators=[DataRequired()])
    next = HiddenField()

    def confirm(self):
        m = sha256()
        m.update(self.password.data.encode())
        user = Utilisateur(self.login.data, m.hexdigest())
        if (self.password.data == self.repeat_password.data and
                len(self.password.data) >= 8 and len(self.login.data) >= 5):
            db.session.add(user)
            db.session.commit()
            return user
        return None
