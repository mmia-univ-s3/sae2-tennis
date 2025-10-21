from appli.app import db
from appli.models import *

class Histoire(db.Model):
    __tablename__ = "HISTOIRE"

    annee:int = db.Column("annee", db.Integer, primary_key = True)
    trivia:str = db.Column("trivia", db.String)

    def __init__(self, annee:int, trivia:str):
        self.annee = annee
        self.trivia = trivia

    def __str__(self):
        return f"<Histoire({self.annee}) {self.trivia}>"
