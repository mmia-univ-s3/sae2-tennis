from datetime import date
from appli.app import db

# pylint: disable=too-many-arguments,too-many-instance-attributes
class Championnat(db.Model):
    """Championnat"""
    __tablename__ = "CHAMPIONNAT"
    id: int = db.Column("idCha", db.Integer, primary_key=True)
    date_championnat: date = db.Column("dateCha", db.Date)
    titre: str = db.Column("titreCha", db.Text)
    type_championnat: str = db.Column("type_championnat", db.Text, nullable=False)

    __mapper_args__ = {"polymorphic_on": type_championnat}

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, date_championnat: date, titre: str):
        self.date_championnat = date_championnat
        self.titre = titre

    def __str__(self):
        return f"<Championnat({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()

# pylint: disable=too-many-arguments,too-many-instance-attributes
class ChampionnatIndividuel(Championnat):
    """Championnat individuel"""
    __mapper_args__ = {"polymorphic_identity": "individuel"}

    __tablename__ = "CHAMP_INDIV"

    id = db.Column("idCha", db.ForeignKey('CHAMPIONNAT.idCha'), primary_key=True)

    categorie: str = db.Column("categorieSport", db.Text)
    serie: str = db.Column("serie", db.Text)
    niveau: str = db.Column("niveau", db.Text)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, date_championnat: date, titre: str, categorie: str, serie: str,
                 niveau: str):
        super().__init__(date_championnat, titre)
        self.categorie = categorie
        self.serie = serie
        self.niveau = niveau

    def vainqueur(self) -> str:
        """Donne le nom du vainqueur du tournoi

        Returns:
            str: Le prénom et nom du vainqueur
        """
        for participant in self.classer:
            if participant.rang.startswith("1"):
                return f"{participant.joueur.prenom} {participant.joueur.nom}"
        return "-"

    def finaliste(self) -> str:
        """Donne le nom du finaliste autre que le vainqueur du tournoi

        Returns:
            str: Le prénom et nom du finaliste
        """
        for participant in self.classer:
            if participant.rang.startswith("2"):
                return f"{participant.joueur.prenom} {participant.joueur.nom}"
        return "-"

    def __str__(self):
        return f"<ChampionnatIndividuel({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()

# pylint: disable=too-many-arguments,too-many-instance-attributes
class ChampionnatEquipe(Championnat):
    """Championnat par équipe"""
    __mapper_args__ = {"polymorphic_identity": "equipe"}

    __tablename__ = "CHAMP_EQUIPE"

    id = db.Column("idCha", db.ForeignKey('CHAMPIONNAT.idCha'), primary_key=True)

    categorie: str = db.Column("categorieSport", db.Text)
    serie: str = db.Column("serie", db.Text)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, date_championnat: date, titre: str, categorie: str, serie: str):
        super().__init__(date_championnat, titre)
        self.categorie = categorie
        self.serie = serie

    def en_cours(self) -> bool:
        """Indique si un championnat par équipe est toujours en cours

        Returns:
            bool: True si le championnat est en cours, False sinon
        """
        for match in self.affronter:
            if match.date_match > date.today():
                return True
        return False

    def __str__(self):
        return f"<ChampionnatEquipe({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()

# pylint: disable=too-many-arguments,too-many-instance-attributes
class ChampionnatInterne(Championnat):
    """Championnats internes au club"""
    __mapper_args__ = {"polymorphic_identity": "interne"}

    __tablename__ = "CHAMP_INTER"

    id = db.Column("idCha", db.ForeignKey('CHAMPIONNAT.idCha'), primary_key=True)

    # pylint: disable=too-many-arguments,too-many-positional-arguments, useless-parent-delegation
    def __init__(self, date_championnat: date, titre: str):
        super().__init__(date_championnat, titre)

    def __str__(self):
        return f"<ChampionnatInterne({self.id}) {self.titre}>"

    def __repr__(self):
        return self.__str__()
