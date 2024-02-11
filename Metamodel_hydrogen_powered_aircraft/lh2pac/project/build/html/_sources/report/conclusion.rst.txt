Conclusion
==========

Ce projet nous a permis d'étudier à quel point le concept d'un avion à hydrogène est réalisable en étudiant 
seulement la masse maximale de l'avion au décollage. 

Pour trouver un design optimal de l'avion, nous avons supposé les valeurs de certains paramètres techniques.
En réalité, même si ces valeurs sont incertaines et pourraient varier, l'impact de ces variations sur 
la fonction objectif est faible. 

Ainsi l'optimisation réalisée dans la partie 1 semble réaliste malgré l'existence d'incertitudes possibles.
Pour réaliser l'étude, nous avons créé un métamodèle de la fonction étudiée h2turbofan ainsi nous avons pu effectuer
plusieurs itérations lors de l'optimisation de ce métamodèle puisque nous avons supposé notre vrai modèle
très coûteux et nous ne pouvons l'évaluer que 30 fois.

Ce métamodèle est une très bonne représentation du vrai modèle (ceci a été prouvé en utilisant certaines métriques),
ainsi nous avons pu conclure que les résultats obtenus en utilisant ce métamodèle peuvent être étendus au vrai modèle.