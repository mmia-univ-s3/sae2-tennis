from flask_login import UserMixin
from appli.app import db

class Utilisateur(db.Model, UserMixin):
    """Administrateur du site"""
    __tablename__ = "UTILISATEUR"

    login: str = db.Column("idU", db.String(32), primary_key=True)
    mdp: str = db.Column("mdp", db.Text)

    def get_id(self):
        return self.login

    def __init__(self, login: str, mdp: str):
        self.login = login
        self.mdp = mdp

    def __str__(self):
        return f"<Utilisateur({self.login}) {self.mdp}>"
