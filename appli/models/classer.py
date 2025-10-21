from appli.app import db

class Classer(db.Model):
    __tablename__ = "CLASSER"

    id_comp:int = db.Column("idComp", db.Integer, db.ForeignKey("COMPETITION.idComp"),
                            primary_key=True)
    competition = db.relationship("Competition", backref=db.backref("classer",
                                    lazy="dynamic", cascade="all, delete-orphan"))
    id_j:int = db.Column("idJ", db.Integer, db.ForeignKey("JOUEUR.idJ"), primary_key=True)
    joueur = db.relationship("Joueur", backref=db.backref("classer",
                            lazy="dynamic", cascade="all, delete-orphan"))
    rang:int = db.Column("rang", db.Integer)

    def __init__(self, id_comp:int, id_j:int, rang:int):
        self.id_comp = id_comp
        self.id_j = id_j
        self.rang = rang

    def __str__(self):
        return f"<Classer({self.id_comp}, {self.id_j}) {self.rang}>"

    def __repr__(self):
        return self.__str__()
