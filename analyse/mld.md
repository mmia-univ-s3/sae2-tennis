IMAGE[<u>nom_fichier</u>, largeur, description]  
ARTICLE[<u>idArt</u>, titreArt, contenu, nbClics, dateArt, typeArt, #nom_fichier]  
HISTOIRE[<u>idH</u>, annee, trivia, #idArt]  
PARTENAIRE[<u>idP</u>, nomP, logo, important, #nom_fichier]  

UTILISATEUR[<u>idU</u>, mdp, role]  
  
CHAMP_INDIV[<u>idCha</u>, dateCha, titreCha, categorieSport, serie, niveau]  
JOUEUR[<u>idJ</u>, nomJ, prenomJ, #idE]  
OPPOSER[<u>#idCha, #idJ, nomAdv, dateMatch</u>, resultat, score estDomicile]  
CLASSER[<u>#idCha, #idJ</u>, rang]  
  
CHAMP_INTER[<u>idCha</u>, dateCha, titreCha]  
JOUER[<u>#idCha, #idJ1, #idJ2</u>, setsGagnants, score1, score2]  

DIVISION[<u>idDiv</u>, intituleDiv]  
CHAMP_EQUIPE[<u>idCha</u>, dateCha, titreCha, categorieSport, serie]  
EQUIPE[<u>idE</u>, nomE, saison, categorieE, #idDiv, rangDiv]  
PARTICIPER[<u>#idCha, #idE</u>, rang, poule]  
AFFRONTER[<u>#idCha, #idE, nomAdv, dateMatch</u>, resultat, score, estDomicile]  

CATEGORIE_TARIF[<u>idCat</u>, ordreCat, intituleCat, #idSp, #idCatParent]  
SPORT[<u>idSp</u>, nomSp, commentaireSp]
TARIF[<u>idT</u>, ordreT, intituleT, #idCat]  
RESERVATION[<u>#idT</u>, montant]  
REDUCTION[<u>#idT</u>, taux, surLicence]  
