# Spécifications fonctionnelles

## Description générale du projet

Le projet consiste à créer un site web pour un club sportif. Le sujet ne mentionne pas d'espace administrateur ou gérant permettant de modifier le site, il n'y a donc qu'un acteur **visiteur**, c'est-à-dire une personne du public qui visite le site pour y consulter des informations.

## Exigences fonctionnelles

* Connexion à une base de données pour récupérer des informations
* Affichage des informations sous forme graphique (schéma, tableau) ou textuelle
* Informations dynamiques (événements) selon la date du jour
* Site web adaptable à tous les écrans

Voir le MCD, MLD et scripts SQL pour la base de données.

## Règles de gestion

* Toutes les pages du site doivent être accessibles à partir des autres pages, donc avec un lien
* Les données telles que les événements doivent être triés par date
* Les fichiers téléchargeables doivent être au format image (JPG, PNG) ou PDF
* Les pages doivent s'adapter à chaque type d'appareil (téléphone, tablette, ordinateur)
* Chaque page et chaque élément d'une page doit être indépendant et pouvoir être mis à jour de façon indépendante

## Interfaces et intéractions

Voir le PDF des maquettes.

## Contraintes non fonctionnelles

* Chaque page doit mettre moins de 100 ms à charger pour ne pas faire fuir les utilisateurs (utiliser la page Réseau de Firefox pour mesurer)
* Pas de sécurité nécessaire car pas de panel administrateur
* Toutes les images doivent être accessibles (utiliser la page Accessibilité de Firefox pour vérifier)
