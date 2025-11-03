from appli.app import db

class CategorieTarif(db.Model):
    __tablename__ = "CATEGORIE_TARIF"

    id: int = db.Column("idCat", db.Integer, primary_key=True)
    sport: str = db.Column("sport", db.Text)
    intitule: str = db.Column("intituleCat", db.Text)
    _id_parent: int = db.Column("idCatParent", db.Integer, db.ForeignKey("CATEGORIE_TARIF.idCat"))

    enfants = db.relationship("CategorieTarif", backref=db.backref("parent", cascade="all", remote_side=[id]))

    def __init__(self, sport: str, intitule: str, id_parent: int=None):
        self.sport = sport
        self.intitule = intitule
        self._id_parent = id_parent

    def __str__(self):
        return f"<CategorieTarif({self.id}) {self.intitule}>"

    def __repr__(self):
        return self.__str__()
