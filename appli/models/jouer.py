from appli.app import db

class Jouer(db.Model):
    """Match entre 2 joueurs dans un championnat interne"""
    __tablename__ = "JOUER"

    _id_championnat: int = db.Column("idCha", db.Integer, db.ForeignKey("CHAMP_INTER.idCha"),
                             primary_key=True)
    _id_j1: int = db.Column("idJ1", db.Integer, db.ForeignKey("JOUEUR.idJ"), primary_key=True)
    _id_j2: int = db.Column("idJ2", db.Integer, db.ForeignKey("JOUEUR.idJ"), primary_key=True)
    sets: int = db.Column("setsGagnants", db.Integer)
    score1: str = db.Column("score1", db.Text)
    score2: str = db.Column("score2", db.Text)

    championnat = db.relationship("ChampionnatInterne", backref=db.backref("jouer",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    joueur1 = db.relationship("Joueur", foreign_keys=[_id_j1], backref=db.backref("jouer1",
                             lazy="dynamic", cascade="all, delete-orphan"))
    joueur2 = db.relationship("Joueur", foreign_keys=[_id_j2], backref=db.backref("jouer2",
                             lazy="dynamic", cascade="all, delete-orphan"))

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, id_championnat: int, id_j1: int, id_j2: int, sets: int,
                 score1: str, score2: str):
        self._id_championnat = id_championnat
        self._id_j1 = id_j1
        self._id_j2 = id_j2
        self.sets = sets
        self.score1 = score1
        self.score2 = score2

    def vainqueur(self):
        """Indique en fonction des scores le vainqueur du match

        Returns:
            Joueur: Le vainqueur du match, None si y'a égalité
        """
        sets1 = self.sets_gagnees_j1()
        sets2 = self.sets_gagnees_j2()
        if sets1 > sets2:
            return self.joueur1
        if sets2 > sets1:
            return self.joueur2
        else:
            return None
    
    def sets_gagnees_j1(self):
        cpt = 0
        for i in range(len(self.score1)):
            if int(self.score1[i]) > int(self.score2[i]):
                cpt += 1
        return cpt

    def sets_gagnees_j2(self):
        cpt = 0
        for i in range(len(self.score2)):
            if int(self.score2[i]) > int(self.score1[i]):
                cpt += 1
        return cpt

    def __str__(self):
        return f"<Jouer({self._id_championnat}, {self._id_j1} vs {self._id_j2})>"

    def __repr__(self):
        return self.__str__()
