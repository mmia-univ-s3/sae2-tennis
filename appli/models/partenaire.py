from appli.app import db

class Partenaire(db.Model):
    """Association/Entreprise partenaire du club"""
    __tablename__ = "PARTENAIRE"

    id: int = db.Column("idP", db.Integer, primary_key = True)
    nom: str = db.Column("nomP", db.Text)
    lien: str = db.Column("lien", db.Text)
    nom_fichier: str|None = db.Column("nom_fichier", db.Text, db.ForeignKey("IMAGE.nom_fichier"))
    important: bool = db.Column("important", db.Boolean)

    logo = db.relationship("Image")

    def __init__(self, nom: str, lien: str, nom_fichier_image: str, important: bool):
        self.nom = nom
        self.lien = lien
        self.nom_fichier = nom_fichier_image
        self.important = important

    def __str__(self):
        return f"<Partenaire({self.id}) {self.nom}>"

    def __repr__(self):
        return self.__str__()
