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

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, date_championnat: date, titre: str, categorie: str, serie: str, niveau: str):
        self.date_championnat = date_championnat
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
