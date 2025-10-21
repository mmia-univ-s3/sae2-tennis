from flask_login import UserMixin
from appli.app import db

class Utilisateur(db.Model, UserMixin):
    __tablename__ = "UTILISATEUR"
    login:str = db.Column("idU", db.String, primary_key=True)
    mdp:str = db.Column("mdp", db.String)

    def __init__(self, login:str, mdp:str):
        self.login = login
        self.mdp = mdp

    def __str__(self):
        return f"<Utilisateur({self.id}) {self.mdp}>"
