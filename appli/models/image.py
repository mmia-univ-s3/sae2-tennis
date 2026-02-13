from appli.app import db

class Image(db.Model):
    """Contient des informations d'une image"""
    __tablename__ = "IMAGE"

    nom_fichier:str = db.Column("nom_fichier", db.Text, primary_key=True)
    largeur:int = db.Column("largeur", db.Integer)
    description:str = db.Column("description", db.Text)

    def __init__(self, nom_image, largeur, description):
        self.nom_fichier = nom_image
        self.largeur = largeur
        self.description = description

    def __str__(self):
        return f"<Image({self.nom}) {self.description}>"

    def __repr__(self):
        return self.__str__()
