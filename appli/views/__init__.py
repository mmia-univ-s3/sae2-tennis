from .articles import article_view, article_create, article_delete, articles
from .autre import autre
from .competitions import calendrier, palmares, tournois, internes
from .contacts import contacts
from .documents import documents
from .ecole import ecole
from .error import e404, e405, e500
from .histoire import histoire_delete, histoire_ajout, histoire
from .index import index
from .logout import deconnexion
from .management import management
from .partenaires import partenaires, partenaire_delete, partenaire_create
from .redirect import club, competitions, formation
from .tarifications import tarifications_tarif_delete, tarifications_tarif_ajout, \
    tarifications_categorie_delete, tarifications_categorie_ajout, \
    tarifications_souscategorie_ajout, tarifications_ajout_tarif_reservation, \
    tarifications_reservations_update, tarifications_reductions_update, \
    tarifications_ajout_tarif_reduction, tarifications
from .users import connexion, utilisateurs_delete, utilisateurs_create, utilisateurs, \
    utilisateurs_reset
