from appli.app import db
from appli.models import *

class Reservation(db.Model):
    __tablename__ = "RESERVATION"

    id:int = db.Column("idT", db.Integer, db.ForeignKey("TARIF.idT", primary_key=True))
    montant:float = db.Column("montant", db.Float)

    tarif = db.relationship("Tarif", backref=db.backref("tarif", lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id:int, montant:float):
        self.id = id
        self.montant = montant
    
    def __str__(self):
        return f"<Reservation({self.id}) {self.tarif.intitule} {self.taux}>"

    def __repr__(self):
        return self.__str__()
