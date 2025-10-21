from appli.app import db

class Reservation(db.Model):
    __tablename__ = "RESERVATION"

    id_tarif:int = db.Column("idT", db.Integer, db.ForeignKey("TARIF.idT", primary_key=True))
    montant:float = db.Column("montant", db.Float)

    tarif = db.relationship("Tarif", backref=db.backref("tarif",
                            lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id_tarif:int, montant:float):
        self.id_tarif = id_tarif
        self.montant = montant

    def __str__(self):
        return f"<Reservation({self.id}) {self.tarif.intitule} {self.taux}>"

    def __repr__(self):
        return self.__str__()
