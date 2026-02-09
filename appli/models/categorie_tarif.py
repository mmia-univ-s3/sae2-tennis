from sqlalchemy import UniqueConstraint, Index, text
from appli.app import db

class CategorieTarif(db.Model):
    """Catégorie ou sous-catégorie d'un tarif"""
    __tablename__ = "CATEGORIE_TARIF"

    id: int = db.Column("idCat", db.Integer, primary_key=True)
    ordre: int = db.Column("ordreCat", db.Integer)
    intitule: str = db.Column("intituleCat", db.Text)
    _id_sport: int = db.Column("idSp", db.Integer, db.ForeignKey("SPORT.idSp"))
    _id_parent: int = db.Column("idCatParent", db.Integer, db.ForeignKey("CATEGORIE_TARIF.idCat"))

    sport = db.relationship("Sport", backref=db.backref("categoriesTarifs",
                                                        lazy="dynamic",
                                                        cascade="all, delete-orphan"))
    enfants = db.relationship("CategorieTarif", backref=db.backref("parent", remote_side=[id]),
                              cascade="all, delete-orphan",)

    __table_args__ = (
        UniqueConstraint("ordreCat", "idCatParent"),
        Index(
            "idCatParentNull",
            "ordreCat",
            unique=True,
            sqlite_where=text("idCatParent IS NULL")
        )
    )

    def __init__(self, ordre: int, intitule: str, id_sport:int, id_parent: int=None):
        self.ordre = ordre
        self.intitule = intitule
        self._id_sport = id_sport
        self._id_parent = id_parent

    def est_sous_categorie(self):
        """Indique si une catégorie est enfant d'une autre catégorie

        Returns:
            bool: True si la catégorie est une sous-catégorie, False sinon
        """
        return self._id_parent is not None

    def __str__(self):
        return f"<CategorieTarif({self.id}) {self.intitule}>"

    def __repr__(self):
        return self.__str__()
