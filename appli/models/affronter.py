from datetime import date
from sqlalchemy import CheckConstraint
from appli.app import db

class Affronter(db.Model):
    __tablename__ = "AFFRONTER"

    _id_championnat: int = db.Column("idCha", db.Integer,
                                    db.ForeignKey("CHAMP_EQUIPE.idCha", primary_key=True))
    _id_equipe1: int = db.Column("idE1", db.Integer,
                                db.ForeignKey("EQUIPE.idE", primary_key=True))
    _id_equipe2: int = db.Column("idE2", db.Integer,
                                db.ForeignKey("EQUIPE.idE", primary_key=True))
    score1: int = db.Column("score1", db.Integer)
    score2: int = db.Column("score2", db.Integer)
    date_match: date = db.Column("dateMatch", db.Date)

    championnat = db.relationship("ChampionnatEquipe", backref=db.backref("affronter",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    equipe1 = db.relationship("Equipe", backref=db.backref("affronter1",
                              lazy="dynamic", cascade="all, delete-orphan"))
    equipe2 = db.relationship("Equipe", backref=db.backref("affronter2",
                              lazy="dynamic", cascade="all, delete-orphan"))

    __table_args__ = (
        CheckConstraint("idE1 != idE2", name="equipes_differentes"),
    )

    def __init__(self, id_championnat: int, ids_equipe: tuple[int], scores: tuple[int]):
        self._id_championnat = id_championnat
        self._id_equipe1, self._id_equipe2 = ids_equipe
        self.score1, self.score2 = scores

    def __str__(self):
        texte = f"<Affronter({self._id_championnat}) {self.equipe1} ({self.score1})" + \
                f" vs {self.equipe2} ({self.score2})>"
        return texte

    def __repr__(self):
        return self.__str__()
