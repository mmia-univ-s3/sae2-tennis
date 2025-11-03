from datetime import date
from appli.app import db

class Article(db.Model):
    __tablename__ = "ARTICLE"

    id: int = db.Column("idArt", db.Integer, primary_key=True)
    titre: str = db.Column("titreArt", db.Text)
    contenu: str = db.Column("contenu", db.Text)
    clics: int = db.Column("nbClics", db.Integer)
    date_publi: date = db.Column("dateArt", db.Date)
    type_article: str = db.Column("typeArt", db.Text)

    def __init__(self, titre: str, contenu: str, date_publi: date, type_article: str):
        self.titre = titre
        self.contenu = contenu
        self.clics = 0
        self.date_publi = date_publi
        self.type_article = type_article

    def __str__(self):
        return f"<Article({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()
