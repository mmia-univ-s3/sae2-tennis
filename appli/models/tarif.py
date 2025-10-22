from appli.app import db

class Tarif(db.Model):
    __tablename__ = "TARIF"

    id: int = db.Column("idT", db.Integer, primary_key=True)
    intitule: str = db.Column("intituleT", db.String)
    _id_cat: int = db.Column("idCat", db.Integer, db.ForeignKey("CATEGORIE.idCat"))

    categorie = db.relationship("Categorie", backref=db.backref("tarif",
                                lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, intitule: str, id_cat: int):
        self.intitule = intitule
        self._id_cat = id_cat

    def __str__(self):
        return f"<Tarif({self.id}) {self.intitule}>"

    def __repr__(self):
        return self.__str__()
