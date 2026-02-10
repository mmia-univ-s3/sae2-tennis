from appli.app import db

class Inscrire(db.Model):
    """Participation d'un joueur dans un championnat interne"""
    __tablename__ = "INSCRIRE"

    _id_championnat: int = db.Column("idCha", db.Integer, db.ForeignKey("CHAMP_INTER.idCha"),
                             primary_key=True)
    _id_j: int = db.Column("idJ", db.Integer, db.ForeignKey("JOUEUR.idJ"), primary_key=True)

    championnat = db.relationship("ChampionnatInterne", backref=db.backref("inscrire",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    joueur = db.relationship("Joueur", backref=db.backref("inscrire",
                            lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id_championnat: int, id_j: int):
        self._id_championnat = id_championnat
        self._id_j = id_j

    def __str__(self):
        return f"<Inscrire({self._id_championnat}, {self._id_j})>"

    def __repr__(self):
        return self.__str__()
