from appli.app import db
from appli.models import *
from datetime import date

class Article(db.Model):
    __tablename__ = "ARTICLE"

    id:int = db.Column("idArt", db.Integer, primary_key=True)
    titre:str = db.Column("titreArt", db.String)
    contenu:str = db.Column("contenu", db.String)
    clics:int = db.Column("nbClics", db.Integer)
    date_publi:date = db.Column("dateArt", db.Date)
    type:str = db.Column("typeArt", db.String)

    def __init__(self, titre:str, contenu:str, clics:int, date_publi:date, type:str):
        self.titre = titre
        self.contenu = contenu
        self.clics = clics
        self.date_publi = date_publi
        self.type = type

    def __str__(self):
        return f"<Article({self.id}) {self.titre}>"
    
    def __repr__(self):
        return self.__str__()
