from appli.app import db

class Participer(db.Model):
    __tablename__ = "PARTICIPER"

    _id_championnat: int = db.Column("idCha", db.Integer,
                                    db.ForeignKey("CHAMP_EQUIPE.idCha", primary_key=True))
    _id_equipe: int = db.Column("idE", db.Integer,
                               db.ForeignKey("EQUIPE.idE", primary_key=True))
    rang: int = db.Column("rang", db.Integer)
    poule: str = db.Column("poule", db.String)

    championnat = db.relationship("ChampionnatEquipe", backref=db.backref("participer",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    equipe = db.relationship("Equipe", backref=db.backref("participer",
                             lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id_cha: int, id_equipe: int, rang: int, poule: int):
        self._id_championnat = id_cha
        self._id_equipe = id_equipe
        self.rang = rang
        self.poule = poule

    def __str__(self):
        return f"<Participer({self._id_championnat}, {self._id_equipe}) {self.poule} {self.rang}>"

    def __repr__(self):
        return self.__str__()
