from appli.app import db

class Reduction(db.Model):
    __tablename__ = "REDUCTION"

    _id_tarif: int = db.Column("idT", db.Integer, db.ForeignKey("TARIF.idT", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    taux: str = db.Column("taux", db.Text)
    cumulable: bool = db.Column("estCumulable", db.Boolean)

    tarif = db.relationship("Tarif", backref=db.backref("reductions",
                            lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id_tarif: int, taux: str, cumulable: bool):
        self._id_tarif = id_tarif
        self.taux = taux
        self.cumulable = cumulable

    def __str__(self):
        return f"<Reduction({self._id_tarif}) {self.tarif.intitule} {self.taux}>"

    def __repr__(self):
        return self.__str__()
