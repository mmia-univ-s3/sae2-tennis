ARTICLE[<u>idArt</u>, titreArt, contenu, nbClics, dateArt, typeArt]  
HISTOIRE[<u>annee</u>, trivia]  
PARTENAIRE[<u>idP</u>, nomP, logo]  

COMPETITION[<u>idComp</u>, dateComp, titreComp]  
JOUEUR[<u>idJ</u>, nomJ, prenomJ]  
CLASSER[<u>#idComp, #idJ</u>, rang]  

CATEGORIE[<u>idCat</u>, sport, intituleCat, #idCatParent]  
TARIF[<u>idT</u>, intituleT, #idCat]  
RESERVATION[<u>#idT</u>, montant]  
REDUCTION[<u>#idT</u>, taux, estCumulable]  

UTILISATEUR[<u>idU</u>, mdp]
