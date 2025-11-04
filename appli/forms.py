from hashlib import sha256

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
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
    logo = StringField('url du logo', validators=[DataRequired()])

    def confirm(self):
        partenaire = Partenaire(self.nom.data, self.logo.data)
        db.session.add(partenaire)
        db.session.commit()
        return partenaire
