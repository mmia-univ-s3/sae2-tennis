from datetime import date
from appli.app import db

class Opposer(db.Model):
    """Match entre 2 joueurs durant un championnat individuel"""
    # pylint: disable=too-many-instance-attributes,duplicate-code
    __tablename__ = "OPPOSER"

    _id_championnat: int = db.Column("idCha", db.Integer,
                                    db.ForeignKey("CHAMP_INDIV.idCha", ondelete="CASCADE",
                                                  onupdate="CASCADE"), primary_key=True)
    _id_joueur: int = db.Column("idJ", db.Integer,
                                db.ForeignKey("JOUEUR.idJ"), primary_key=True)
    adversaire: str = db.Column("nomAdv", db.String(100))
    date_match: date = db.Column("dateMatch", db.Date, primary_key=True)
    resultat: str = db.Column("resultat", db.Text)
    score: int = db.Column("score", db.Text)
    domicile: bool = db.Column("estDomicile", db.Boolean)

    championnat = db.relationship("ChampionnatIndividuel", backref=db.backref("opposer",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    joueur = db.relationship("Joueur", backref=db.backref("opposer",
                              lazy="dynamic", cascade="all, delete-orphan"))

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, id_championnat: int, id_joueur: int, adversaire: str,
                 resultat: str, score: str,
                 domicile: bool, date_match: date):
        self._id_championnat = id_championnat
        self._id_joueur = id_joueur
        self.adversaire = adversaire
        self.resultat = resultat
        self.score = score
        self.domicile = domicile
        self.date_match = date_match

    def __str__(self):
        texte = f"<Opposer({self._id_championnat}) {self.joueur.nom} vs " + \
                f"{self.adversaire} ({self.resultat})>"
        return texte

    def __repr__(self):
        return self.__str__()
