from appli.app import db

class Joueur(db.Model):
    __tablename__ = "JOUEUR"

    id:int = db.Column("idJ", db.Integer, primary_key=True)
    nom:str = db.Column("nomJ", db.String)
    prenom:str = db.Column("prenomJ", db.String)

    def __init__(self, nom:str, prenom:str):
        self.nom = nom
        self.prenom = prenom

    def __str__(self):
        return f"<Joueur({self.id}) {self.nom} {self.prenom}>"

    def __repr__(self):
        return self.__str__()
