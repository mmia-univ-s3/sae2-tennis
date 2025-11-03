from hashlib import sha256

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
# from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

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
        else:
            return None

class ConfirmForm(FlaskForm):
    pass
