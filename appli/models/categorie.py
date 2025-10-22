from appli.app import db

class Categorie(db.Model):
    __tablename__ = "CATEGORIE"

    id: int = db.Column("idCat", db.Integer, primary_key=True)
    sport: str = db.Column("sport", db.String)
    intitule: str = db.Column("intituleCat", db.String)
    _id_parent: int = db.Column("idCatParent", db.Integer, db.ForeignKey("CATEGORIE.idCat"))

    parent = db.relationship("Categorie", backref=db.backref("enfant",
                             lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, sport: str, intitule: str, id_parent: int=None):
        self.sport = sport
        self.intitule = intitule
        self._id_parent = id_parent

    def __str__(self):
        return f"<Categorie({self.id}) {self.intitule}>"

    def __repr__(self):
        return self.__str__()
