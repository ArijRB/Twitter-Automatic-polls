# Twitter-Automatic-polls
NLP / Community graphs

### Projet réalisé par :
Kim-Anh Laura Nguyen et Arij Riabi
### Promo DAC 2018-2019
### Encadrants :
Vincent Guigue <br/>
Nicolas Baskiotis

### Résumé :
Nous disposons d’une base de données non supervisée constituée de plus de cinq millions de
tweets collectés durant le premier tour des élections présidentielles françaises de 2017 et s’étalant
sur une période de deux jours. En plus du contenu textuel, nous avons également accès à des
métadonnées : nous savons, par exemple, quels utilisateurs sont concernés par un tweet et quels
candidats sont mentionnés dans un tweet. De plus, d’autres jeux de données étiquetées en fonction
des sentiments sont à notre disposition : des critiques de films, des tweets traduits de l’anglais au
français ainsi que des avis sur des produits Décathlon.
À partir de la base de tweets collectés durant les élections présidentielles, nous souhaitons dé-
terminer les sentiments ainsi que les opinions politiques des utilisateurs.
Pour répondre à notre problématique, nous avons suivi la démarche suivante. Nous considére-
rons d’abord une approche classique en traitement automatique des langues avec transfert d’un
classifieur de sentiments appris sur des sources étiquetées vers les données textuelles Twitter. Nous
étudierons ensuite ces questions en exploitant, non pas le contenu textuel, mais les interactions
entre utilisateurs en construisant un graphe de communautés. Enfin, nous fusionnerons les deux
approches dans l’objectif d’apprendre un modèle de classification de sentiments sur des données
faiblement supervisées.
## Table des matières
# 1 Introduction
# 2 Analyse de sentiments et transfert
2.1 Apprentissage sur des critiques de films 
2.2 Apprentissage sur des tweets traduits
2.3 Application des modèles sur d’autres données étiquetées 
2.4 Application des modèles sur les tweets des élections présidentielles
# 3 Analyse de communautés
# 4 Fusion des deux approches
4.1 Classification de sentiments 
4.2 Prédiction d’opinions 
4.3 Bilan .
# 5 Conclusion et perspectives 
