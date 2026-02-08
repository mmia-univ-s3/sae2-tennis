from appli.app import db

class Sport(db.Model):
    """Un sport pratiqué au sein du club"""
    __tablename__ = "SPORT"

    id: int = db.Column("idSp", db.Integer, primary_key = True)
    nom: str = db.Column("nomSp", db.Text)
    commentaire: str = db.Column("commentaireSp", db.Text)

    def __init__(self, nom: int, commentaire: str):
        self.nom = nom
        self.commentaire = commentaire

    def __str__(self):
        return f"<Sport({self.id}) {self.nom}>"
    
    def __repr__(self):
        return self.__str__()