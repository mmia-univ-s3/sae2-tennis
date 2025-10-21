from appli.app import db
from appli.models import *

class Partenaire(db.Model):
    __tablename__ = "PARTENAIRE"

    id:int = db.Column("idP", db.Integer, primary_key = True)
    nom:str = db.Column("nomP", db.String)
    logo:str = db.Column("logo", db.String)

    def __init__(self, nom:str, logo:str):
        self.nom = nom
        self.logo = logo

    def __str__(self):
        return f"<Partenaire({self.id}) {self.nom}>"

    def __repr__(self):
        return self.__str__()
