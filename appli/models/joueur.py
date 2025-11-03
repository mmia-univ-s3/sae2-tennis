from appli.app import db

class Joueur(db.Model):
    __tablename__ = "JOUEUR"

    id: int = db.Column("idJ", db.Integer, primary_key=True)
    nom: str = db.Column("nomJ", db.Text)
    prenom: str = db.Column("prenomJ", db.Text)
    _id_equipe: int = db.Column("idE", db.Integer, db.ForeignKey("EQUIPE.idE"))

    equipe = db.relationship("Equipe", backref=db.backref("enfant",
                             lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, nom: str, prenom: str, id_equipe: int):
        self.nom = nom
        self.prenom = prenom
        self._id_equipe = id_equipe

    def __str__(self):
        return f"<Joueur({self.id}) {self.nom} {self.prenom}>"

    def __repr__(self):
        return self.__str__()
