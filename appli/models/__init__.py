from appli.app import login_manager
from appli.models.utilisateur import Utilisateur

@login_manager.user_loader
def load_user(login: str):
    return Utilisateur.query.get(login)
