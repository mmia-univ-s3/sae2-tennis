from appli.app import db

class Histoire(db.Model):
    __tablename__ = "HISTOIRE"

    annee:int = db.Column("annee", db.Integer, primary_key = True)
    trivia:str = db.Column("trivia", db.String)

    def __init__(self, annee:int, trivia:str):
        self.annee = annee
        self.trivia = trivia

    def __str__(self):
        return f"<Histoire({self.annee}) {self.trivia}>"

    def __repr__(self):
        return self.__repr__()
