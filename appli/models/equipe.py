from appli.app import db

class Equipe(db.Model):
    __tablename__ = "EQUIPE"

    id: int = db.Column("idE", db.Integer, primary_key=True)
    nom: str = db.Column("nomE", db.Text)
    categorie: str = db.Column("categorieE", db.Text)
    _id_div: int = db.Column("idDiv", db.Integer, db.ForeignKey("DIVISION.idDiv"))
    rang: int = db.Column("rang", db.Integer)

    division = db.relationship("Division", backref=db.backref("equipe",
                               lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, nom: str, categorie: str, id_div: int, rang: int):
        self.nom = nom
        self.categorie = categorie
        self._id_div = id_div
        self.rang = rang

    def __str__(self):
        return f"<Equipe({self.id}) {self.nom}>"

    def __repr__(self):
        return self.__str__()
