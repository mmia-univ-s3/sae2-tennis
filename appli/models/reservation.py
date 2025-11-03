from appli.app import db

class Reservation(db.Model):
    __tablename__ = "RESERVATION"

    _id_tarif: int = db.Column("idT", db.Integer, db.ForeignKey("TARIF.idT", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    montant: float = db.Column("montant", db.Float)

    tarif = db.relationship("Tarif", backref=db.backref("reservations",
                            lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id_tarif: int, montant: float):
        self._id_tarif = id_tarif
        self.montant = montant

    def __str__(self):
        return f"<Reservation({self._id_tarif}) {self.tarif.intitule} {self.montant}>"

    def __repr__(self):
        return self.__str__()
