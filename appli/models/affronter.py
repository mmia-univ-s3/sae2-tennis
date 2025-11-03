from datetime import date
from appli.app import db

class Affronter(db.Model):
    # pylint: disable=too-many-instance-attributes,duplicate-code
    __tablename__ = "AFFRONTER"

    _id_championnat: int = db.Column("idCha", db.Integer,
                                    db.ForeignKey("CHAMP_EQUIPE.idCha", ondelete="CASCADE",
                                                  onupdate="CASCADE"), primary_key=True)
    _id_equipe: int = db.Column("idE", db.Integer,
                                db.ForeignKey("EQUIPE.idE"), primary_key=True)
    adversaire: str = db.Column("nomAdv", db.Text, primary_key=True)
    resultat: str = db.Column("resultat", db.Text)
    score: int = db.Column("score", db.Text)
    stade: str = db.Column("stade", db.Text)
    domicile: bool = db.Column("estDomicile", db.Boolean)
    date_match: date = db.Column("dateMatch", db.Date)

    championnat = db.relationship("ChampionnatEquipe", backref=db.backref("affronter",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    equipe = db.relationship("Equipe", backref=db.backref("affronter",
                              lazy="dynamic", cascade="all, delete-orphan"))

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, id_championnat: int, id_equipe: int, adversaire: str,
                 resultat: str, score: str,
                 stade: str, domicile: bool, date_match: date):
        self._id_championnat = id_championnat
        self._id_equipe = id_equipe
        self.adversaire = adversaire
        self.resultat = resultat
        self.score = score
        self.stade = stade
        self.domicile = domicile
        self.date_match = date_match

    def __str__(self):
        texte = f"<Affronter({self._id_championnat}) {self.equipe.nom} vs " + \
                f"{self.adversaire} ({self.resultat})>"
        return texte

    def __repr__(self):
        return self.__str__()
