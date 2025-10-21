from datetime import date
from appli.app import db

class Competition(db.Model):
    __tablename__ = "COMPETITION"

    id:int = db.Column("idComp", db.Integer, primary_key=True)
    date_comp:date = db.Column("dateComp", db.Date)
    titre:str = db.Column("titreComp", db.String)

    def __init__(self, date_comp:date, titre:str):
        self.date_comp = date_comp
        self.titre = titre

    def __str__(self):
        return f"<Competition({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()
