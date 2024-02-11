Introduction
============

Dans un contexte actuel où les émissions de gaz à effet de serre sont au coeur des enjeux environnementaux, 
transformer le monde de l'aviation est une nécessité.

En effet, remplacer le kérozène utilisé pour faire voler les avions par de l'hydrogène est une piste intéressante, 
étant donné que l'hydrogène n'émet pas de dioxyde de carbone, qui est un des principaux gaz à effet de serre. 
C'est dans ce contexte que s'inscrit ce projet, qui consiste à créer un design d'avion à hydrogène à partir 
d'un simulateur numérique, la fonction H2TurboFan. Cependant, le modèle du simulateur étant très coûteux, 
le nombre d'évaluations est limité à 30 évaluations. 
Le design doit également satisfaire les caractéristiques classiques d'un avion A320 à kérozène. 

Afin de créer le meilleur design possible, on cherche à minimiser le poids maximum au décollage 
(Maximum Take Off Weight (MTOW)). Pour ce faire, le problème se divise en deux parties : dans un premier
temps, puisque le modèle est coûteux, des modèles de surrogates approchant au maximum le vrai modèle
seront utilisés et optimisés. Puis dans un second temps, nous introduirons des incertitudes sur 
les paramètres techniques du modèle afin d'observer leur répercussion sur la phase d'optimisation. 
Nous quantifierons cette sensibilité aux incertitudes à l'aide de métriques telles que les indices de Sobol.


