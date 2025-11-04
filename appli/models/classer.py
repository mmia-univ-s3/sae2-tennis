from appli.app import db

class Classer(db.Model):
    __tablename__ = "CLASSER"

    _id_championnat: int = db.Column("idCha", db.Integer, db.ForeignKey("CHAMP_INDIV.idCha"),
                             primary_key=True)
    _id_j: int = db.Column("idJ", db.Integer, db.ForeignKey("JOUEUR.idJ"), primary_key=True)
    rang: int = db.Column("rang", db.Integer)

    competition = db.relationship("ChampionnatIndividuel", backref=db.backref("classer",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    joueur = db.relationship("Joueur", backref=db.backref("classer",
                            lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id_championnat: int, id_j: int, rang: int):
        self._id_championnat = id_championnat
        self._id_j = id_j
        self.rang = rang

    def __str__(self):
        return f"<Classer({self._id_championnat}, {self._id_j}) {self.rang}>"

    def __repr__(self):
        return self.__str__()
