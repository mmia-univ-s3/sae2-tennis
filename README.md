# SAE Stade Poitevin Tennis

## Installation

### Sur Linux ou macOS

```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Sur Windows (PowerShell)

```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Pour exécuter

```
flask run
```

Ou si vous devez modifier l'URL de la base de données :

#### Sur Linux ou macOS

```
DATABASE_URL=mysql://nomutilisateur:motdepasse@serveur/BaseDeDonnees flask run
```

#### Sur Windows

```
$Env:DATABASE_URL = "mysql://nomutilisateur:motdepasse@serveur/BaseDeDonnees"
flask run
```

## Description générale du projet

Le projet consiste à créer un site web pour un club sportif. Il y a donc un acteur **visiteur**, c'est-à-dire une personne du public qui visite le site pour y consulter des informations, ainsi qu'un acteur **administrateur** qui permet de gérer le site et son contenu.

## Exigences fonctionnelles

* Connexion à une base de données pour récupérer des informations
* Affichage des informations sous forme graphique (schéma, tableau) ou textuelle
* Informations dynamiques (événements) selon la date du jour
* Site web adaptable à tous les écrans
* Modification facile sans modifier le code

Voir le MCD, MLD et scripts Python (`models`) pour la base de données.

## Règles de gestion

* Toutes les pages du site doivent être accessibles à partir des autres pages, donc avec un lien
* Les données telles que les événements doivent être triés par date
* Les fichiers téléchargeables doivent être au format image (JPG, PNG) ou PDF
* Les pages doivent s'adapter à chaque type d'appareil (téléphone, tablette, ordinateur)
* Chaque page et chaque élément d'une page doit être indépendant et pouvoir être mis à jour de façon indépendante
* La cohérence du contenu doit être vérifiée avant sa publication

## Interfaces et intéractions

Voir le PDF des maquettes.

## Contraintes non fonctionnelles

* Chaque page doit mettre moins de 100 ms à charger pour ne pas faire fuir les utilisateurs (utiliser la page Réseau de Firefox pour mesurer)
* Mots de passes chiffrés et pages d'administrateur bloquées derrière une authentification
* Toutes les images doivent être accessibles (utiliser la page Accessibilité de Firefox pour vérifier)
