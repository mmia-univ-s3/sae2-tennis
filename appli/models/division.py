from appli.app import db

class Division(db.Model):
    __tablename__ = "DIVISION"

    id: int = db.Column("idDiv", db.Integer, primary_key=True)
    intitule: str = db.Column("intituleDiv", db.Text)

    def __init__(self, intitule: str):
        self.intitule = intitule

    def __str__(self):
        return f"<Division({self.id}) {self.intitule}>"

    def __repr__(self):
        return self.__str__()
