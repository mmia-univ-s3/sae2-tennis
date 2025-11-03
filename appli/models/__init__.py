from appli.app import login_manager

from .article import Article
from .histoire import Histoire
from .partenaire import Partenaire
from .utilisateur import Utilisateur
from .division import Division
from .joueur import Joueur
from .classer import Classer
from .championnat import ChampionnatEquipe, ChampionnatIndividuel
from .equipe import Equipe
from .participer import Participer
from .affronter import Affronter
from .categorie_tarif import CategorieTarif
from .tarif import Tarif
from .reservation import Reservation
from .reduction import Reduction

@login_manager.user_loader
def load_user(_: str):
    pass
