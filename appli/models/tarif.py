from appli.app import db

class Tarif(db.Model):
    """Infos du tarif"""
    __tablename__ = "TARIF"

    id: int = db.Column("idT", db.Integer, primary_key=True)
    intitule: str = db.Column("intituleT", db.Text)
    _id_cat: int = db.Column("idCat", db.Integer, db.ForeignKey("CATEGORIE_TARIF.idCat"))
    type_tarif: str = db.Column("type_tarif", db.String, nullable=False)

    categorie = db.relationship("CategorieTarif", backref=db.backref("tarifs",
                                lazy="dynamic", cascade="all, delete-orphan"))
    
    __mapper_args__ = {"polymorphic_on": type_tarif}

    def __init__(self, intitule: str, id_cat: int):
        self.intitule = intitule
        self._id_cat = id_cat

    def __str__(self):
        return f"<Tarif({self.id}) {self.intitule}>"

    def __repr__(self):
        return self.__str__()

class Reduction(Tarif):
    """Réduction dans les tarifs"""
    __mapper_args__ = {"polymorphic_identity": "reduction"}

    taux: str = db.Column("taux", db.Text)
    licence: bool = db.Column("surLicence", db.Boolean)

    def __init__(self, intitule: str, id_cat: int, taux: str, licence: bool):
        super().__init__(intitule, id_cat)
        self.taux = taux
        self.licence = licence

    def __str__(self):
        return f"<Reduction({self._id_tarif}) {self.tarif.intitule} {self.taux}>"

    def __repr__(self):
        return self.__str__()

class Reservation(Tarif):
    """Prix d'un tarif"""
    __mapper_args__ = {"polymorphic_identity": "reservation"}

    montant: float = db.Column("montant", db.Float)

    def __init__(self, intitule: str, id_cat: int, montant: float):
        super().__init__(intitule, id_cat)
        self.montant = montant

    def __str__(self):
        return f"<Reservation({self._id_tarif}) {self.tarif.intitule} {self.montant}>"

    def __repr__(self):
        return self.__str__()