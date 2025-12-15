from datetime import date
from appli.app import db

class ChampionnatIndividuel(db.Model):
    __tablename__ = "CHAMP_INDIV"

    id: int = db.Column("idCha", db.Integer, primary_key=True)
    date_championnat: date = db.Column("dateCha", db.Date)
    titre: str = db.Column("titreCha", db.Text)
    categorie: str = db.Column("categorieSport", db.Text)
    serie: str = db.Column("serie", db.Text)
    niveau: str = db.Column("niveau", db.Text)

    _id_joueur_1: int = db.Column("idJ1", db.Integer, db.ForeignKey("JOUEUR.idJ"))
    _id_joueur_2: int = db.Column("idJ2", db.Integer, db.ForeignKey("JOUEUR.idJ"))
    joueur_1 = db.Relationship("Joueur", foreign_keys=[_id_joueur_1], backref=db.backref(
        "championnats_j1", lazy="dynamic", cascade="all, delete-orphan"))
    joueur_2 = db.Relationship("Joueur", foreign_keys=[_id_joueur_2], backref=db.backref(
        "championnats_j2", lazy="dynamic", cascade="all, delete-orphan"))

    score_1: int = db.Column("score1", db.Integer)
    score_2: int = db.Column("score2", db.Integer)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, date_championnat: date, titre: str, categorie: str, serie: str, niveau: str,
                 id_joueur_1: int, id_joueur_2: int, score_1: int, score_2: int):
        self.date_championnat = date_championnat
        self.titre = titre
        self.categorie = categorie
        self.serie = serie
        self.niveau = niveau
        self._id_joueur_1 = id_joueur_1
        self._id_joueur_2 = id_joueur_2
        self.score_1 = score_1
        self.score_2 = score_2

    def __str__(self):
        return f"<ChampionnatIndividuel({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()

class ChampionnatEquipe(db.Model):
    __tablename__ = "CHAMP_EQUIPE"

    id: int = db.Column("idCha", db.Integer, primary_key=True)
    date_championnat: date = db.Column("dateCha", db.Date)
    titre: str = db.Column("titreCha", db.Text)
    categorie : str = db.Column("categorieSport", db.Text)
    serie : str = db.Column("serie", db.Text)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, date_championnat: date, titre: str, categorie: str, serie: str):
        self.date_championnat = date_championnat
        self.titre = titre
        self.categorie = categorie
        self.serie = serie

    def __str__(self):
        return f"<ChampionnatEquipe({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()
