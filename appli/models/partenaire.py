from appli.app import db

class Partenaire(db.Model):
    """Association/Entreprise partenaire du club"""
    __tablename__ = "PARTENAIRE"

    id: int = db.Column("idP", db.Integer, primary_key = True)
    nom: str = db.Column("nomP", db.Text)
    lien: str = db.Column("lien", db.Text)
    nom_fichier: str = db.Column("nom_fichier", db.Text, db.ForeignKey("IMAGE.nom_fichier"))

    logo = db.relationship("Image")

    def __init__(self, nom: str, lien: str, nom_fichier_image: str):
        self.nom = nom
        self.lien = lien
        self.nom_fichier = nom_fichier_image

    def __str__(self):
        return f"<Partenaire({self.id}) {self.nom}>"

    def __repr__(self):
        return self.__str__()
