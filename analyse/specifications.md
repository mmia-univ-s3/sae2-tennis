# Spécifications fonctionnelles

## Description générale du projet

Le projet consiste à créer un site web pour un club sportif. Le sujet ne mentionne pas d'espace administrateur ou gérant permettant de modifier le site, il n'y a donc qu'un acteur **visiteur**, c'est-à-dire une personne du public qui visite le site pour y consulter des informations.

## Exigences fonctionnelles

Fonctions principales :

* Connexion à une base de données pour récupérer des informations
* Affichage des informations sous forme graphique (schéma, tableau) ou textuelle
* Informations dynamiques (événements) selon la date du jour
* Site web adaptable à tous les écrans

Voir le MCD, MLD et scripts SQL pour la base de données.

## Règles de gestion

-

## Interfaces et intéractions

Voir le PDF des maquettes.

## Contraintes non fonctionnelles

* Chaque page doit mettre moins de 100 ms à charger pour ne pas faire fuir les utilisateurs (utiliser la page Réseau de Firefox pour mesurer)
* Pas de sécurité nécessaire car pas de panel administrateur
* Toutes les images doivent être accessibles (utiliser la page Accessibilité de Firefox pour vérifier)
