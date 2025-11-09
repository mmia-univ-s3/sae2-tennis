from appli.app import db

class Participer(db.Model):
    """Participation/Classement d'une équipe dans un championnat par équipe"""
    __tablename__ = "PARTICIPER"

    _id_championnat: int = db.Column("idCha", db.Integer,
                                    db.ForeignKey("CHAMP_EQUIPE.idCha", ondelete="CASCADE",
                                                  onupdate="CASCADE"), primary_key=True)
    _id_equipe: int = db.Column("idE", db.Integer,
                               db.ForeignKey("EQUIPE.idE"), primary_key=True)
    rang: str = db.Column("rang", db.Text)
    poule: str = db.Column("poule", db.Text)

    championnat = db.relationship("ChampionnatEquipe", backref=db.backref("participer",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    equipe = db.relationship("Equipe", backref=db.backref("participer",
                             lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id_championnat: int, id_equipe: int, rang: str, poule: int):
        self._id_championnat = id_championnat
        self._id_equipe = id_equipe
        self.rang = rang
        self.poule = poule

    def __str__(self):
        return f"<Participer({self._id_championnat}, {self._id_equipe}) {self.poule} {self.rang}>"

    def __repr__(self):
        return self.__str__()
