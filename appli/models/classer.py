from appli.app import db

class Classer(db.Model):
    """Participation/Classement d'un joueur dans un championnat individuel"""
    __tablename__ = "CLASSER"

    _id_championnat: int = db.Column("idCha", db.Integer, db.ForeignKey("CHAMP_INDIV.idCha"),
                             primary_key=True)
    _id_j: int = db.Column("idJ", db.Integer, db.ForeignKey("JOUEUR.idJ"), primary_key=True)
    rang: str = db.Column("rang", db.Text)

    championnat = db.relationship("ChampionnatIndividuel", backref=db.backref("classer",
                                  lazy="dynamic", cascade="all, delete-orphan"))
    joueur = db.relationship("Joueur", backref=db.backref("classer",
                            lazy="dynamic", cascade="all, delete-orphan"))

    def __init__(self, id_championnat: int, id_j: int, rang: str):
        self._id_championnat = id_championnat
        self._id_j = id_j
        self.rang = rang

    def classement(self):
        """Permet d'afficher le classement du joueur au format texte

        Returns:
            str: Le classement du joueur
        """
        match self.rang:
            case "1":
                classement_texte = "Vainqueur"
            case "2":
                classement_texte =  "Finaliste"
            case "4":
                classement_texte =  "Demi-finaliste"
            case "8":
                classement_texte =  "Quart de finale"
            case "16":
                classement_texte =  "Huitième de finale"
            case "32":
                classement_texte =  "Seizième de finale"
            case _:
                classement_texte =  "Poule"
        return classement_texte

    def __str__(self):
        return f"<Classer({self._id_championnat}, {self._id_j}) {self.rang}>"

    def __repr__(self):
        return self.__str__()
