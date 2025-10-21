from appli.app import db
from appli.models import *
from flask_login import UserMixin

class Utilisateur(db.Model, UserMixin):
    __tablename__ = "UTILISATEUR"
    id:str = db.Column("idU", db.String, primary_key=True)
    mdp:str = db.Column("mdp", db.String)

    def __init__(self, id:str, mdp:str):
        self.id = id
        self.mdp = mdp

    def __str__(self):
        return f"<Utilisateur({self.id}) {self.mdp}>"
