from appli.app import db

class Partenaire(db.Model):
    """Association/Entreprise partenaire du club"""
    __tablename__ = "PARTENAIRE"

    id: int = db.Column("idP", db.Integer, primary_key = True)
    nom: str = db.Column("nomP", db.Text)
    logo: str = db.Column("logo", db.Text)
    lien: str = db.Column("lien", db.Text)
    important: bool = db.Column("important", db.Boolean)

    def __init__(self, nom: str, logo: str, lien: str, important: bool):
        self.nom = nom
        self.logo = logo
        self.lien = lien
        self.important = important

    def __str__(self):
        return f"<Partenaire({self.id}) {self.nom}>"

    def __repr__(self):
        return self.__str__()
