from appli.app import db

class Histoire(db.Model):
    """Trivia du club"""
    __tablename__ = "HISTOIRE"

    id: int = db.Column("idH", db.Integer, primary_key = True)
    annee: int = db.Column("annee", db.Integer)
    trivia: str = db.Column("trivia", db.Text)
    article: int|None = db.Column("article", db.Integer, db.ForeignKey("ARTICLE.idArt"))

    def __init__(self, annee: int, trivia: str, article:int|None):
        self.annee = annee
        self.trivia = trivia
        self.article = article

    def __str__(self):
        return f"<Histoire({self.id}) {self.annee} lié à {self.article}>"

    def __repr__(self):
        return self.__str__()
