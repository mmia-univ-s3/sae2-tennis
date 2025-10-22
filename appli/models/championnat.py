from datetime import date
from appli.app import db

class ChampionnatIndividuel(db.Model):
    __tablename__ = "CHAMP_INDIV"

    id: int = db.Column("idCha", db.Integer, primary_key=True)
    date_comp: date = db.Column("dateCha", db.Date)
    titre: str = db.Column("titreCha", db.String)
    categorie : str = db.Column("categorieSport", db.String)
    serie : str = db.Column("serie", db.String)
    niveau : str = db.Column("niveau", db.String)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, date_comp: date, titre: str, categorie: str, serie: str, niveau: str):
        self.date_comp = date_comp
        self.titre = titre
        self.categorie = categorie
        self.serie = serie
        self.niveau = niveau

    def __str__(self):
        return f"<ChampionnatIndividuel({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()

class ChampionnatEquipe(db.Model):
    __tablename__ = "CHAMP_EQUIPE"

    id: int = db.Column("idCha", db.Integer, primary_key=True)
    date_comp: date = db.Column("dateCha", db.Date)
    titre: str = db.Column("titreCha", db.String)
    categorie : str = db.Column("categorieSport", db.String)
    serie : str = db.Column("serie", db.String)
    id_div : int = db.Column("idDiv", db.Integer, db.ForeignKey("DIVISION.idDiv"))

    division = db.relationship("Division", backref=db.backref("championnat",
                               lazy="dynamic", cascade="all, delete-orphan"))

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, date_comp: date, titre: str, categorie: str, serie: str, id_div: int):
        self.date_comp = date_comp
        self.titre = titre
        self.categorie = categorie
        self.serie = serie
        self.id_div = id_div

    def __str__(self):
        return f"<ChampionnatEquipe({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()
