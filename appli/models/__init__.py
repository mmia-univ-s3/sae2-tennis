from appli.app import login_manager
from appli.models.utilisateur import Utilisateur

from .article import Article
from .histoire import Histoire
from .partenaire import Partenaire
from .utilisateur import Utilisateur
from .division import Division
from .joueur import Joueur
from .classer import Classer
from .championnat import ChampionnatEquipe, ChampionnatIndividuel, Championnat
from .equipe import Equipe
from .participer import Participer
from .affronter import Affronter
from .categorie_tarif import CategorieTarif
from .tarif import Tarif, Reservation, Reduction
from .sport import Sport

@login_manager.user_loader
def load_user(login: str):
    """Récupère un utilisateur à partir de son identifiant"""
    return Utilisateur.query.get(login)
