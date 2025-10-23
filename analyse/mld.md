ARTICLE[<u>idArt</u>, titreArt, contenu, nbClics, dateArt, typeArt]  
HISTOIRE[<u>idH</u>, annee, trivia]  
PARTENAIRE[<u>idP</u>, nomP, logo]  
UTILISATEUR[<u>idU</u>, mdp]  

CHAMP_INDIV[<u>idCha</u>, dateCha, titreCha, categorieSport, serie, niveau]  
JOUEUR[<u>idJ</u>, nomJ, prenomJ, #idE]  
CLASSER[<u>#idCha, #idJ</u>, rang]  

DIVISION[<u>idDiv</u>, intituleDiv]  
CHAMP_EQUIPE[<u>idCha</u>, dateCha, titreCha, categorieSport, serie, #idDiv]  
EQUIPE[<u>idE</u>, nomE, categorieE, #idDiv, rangDiv]  
PARTICIPER[<u>#idCha, #idE</u>, rang, poule]  
AFFRONTER[<u>#idCha, #idE</u>, nomAdv, resultat, score, stade, estDomicile, dateMatch]

CATEGORIE_TARIF[<u>idCat</u>, sport, intituleCat, #idCatParent]  
TARIF[<u>idT</u>, intituleT, #idCat]  
RESERVATION[<u>#idT</u>, montant]  
REDUCTION[<u>#idT</u>, taux, estCumulable]  
