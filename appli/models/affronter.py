from datetime import date
from appli.app import db

class Affronter(db.Model):
    __tablename__ = "AFFRONTER"

    id_championnat: int = db.Column("idCha", db.Integer, 
                                    db.ForeignKey("CHAMP_EQUIPE.idCha", primary_key=True))
    id_equipe1: int = db.Column("idE1", db.Integer,
                                db.ForeignKey("EQUIPE.idE", primary_key=True))
    id_equipe2: int = db.Column("idE2", db.Integer,
                                db.ForeignKey("EQUIPE.idE", primary_key=True))
    score1: int = db.Column("score1", db.Integer)
    score2: int = db.Column("score2", db.Integer)
    date_match: date = db.Column("dateMatch", db.Date)

    championnat = db.relationship("Championnat_Equipe", backref=db.backref("affronter",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    equipe1 = db.relationship("Equipe", backref=db.backref("affronter1",
                              lazy="dynamic", cascade="all, delete-orphan"))
    equipe2 = db.relationship("Equipe", backref=db.backref("affronter2",
                              lazy="dynamic", cascade="all, delete-orphan"))

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, id_cha: int, ids_equipe: tuple[int], scores: tuple[int]):
        