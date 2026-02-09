from flask_login import UserMixin
from appli.app import db, get_role_permission_lvl


class Utilisateur(db.Model, UserMixin):
    """Administrateur du site"""
    __tablename__ = "UTILISATEUR"

    login: str = db.Column("idU", db.String(32), primary_key=True)
    mdp: str = db.Column("mdp", db.Text)
    role: str = db.Column("role", db.Text)

    def get_id(self):
        """Renvoie l'identifiant.
        
        Returns:
            L'identifiant."""
        return self.login

    def __init__(self, login: str, mdp: str, role: str):
        self.login = login
        self.mdp = mdp
        self.role = role

    def role_au_moins(self, role):
        """
        Vérifie si le rôle de l'utilisateur est au moins aussi permissif que le rôle requis.

        Returns:
            True si le rôle correspond, False sinon
        """
        return get_role_permission_lvl(self.role) >= get_role_permission_lvl(role)

    def __str__(self):
        return (f"<Utilisateur({self.login}) {self.role}({get_role_permission_lvl(self.role)}) "
                f"{self.mdp}>")
