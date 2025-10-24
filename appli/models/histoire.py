from appli.app import db

class Histoire(db.Model):
    __tablename__ = "HISTOIRE"

    id: int = db.Column("idH", db.Integer, primary_key = True)
    annee: int = db.Column("annee", db.Integer)
    trivia: str = db.Column("trivia", db.String)

    def __init__(self, annee: int, trivia: str):
        self.annee = annee
        self.trivia = trivia

    def __str__(self):
        return f"<Histoire({self.id}) {self.annee}>"

    def __repr__(self):
        return self.__repr__()
