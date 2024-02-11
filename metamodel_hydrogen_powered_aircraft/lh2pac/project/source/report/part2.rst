Métamodélisation et quantification des incertitudes
===================================================

Coefficients de variation des variables en entrée
--------------------------------------------------

Dans la première partie, nous avions construit un design d'avion avec des paramètres fixés, 
tandis que dans cette partie, les paramètres techniques sont incertains et suivent
une loi triangulaire. L'objectif de cette partie est d'observer à quel
point notre modèle est sensible aux variations des paramètres en entrée :
"tgi","tvi","sfc","mass","drag".

Pour ce faire, nous commençons par calculer le coefficient de variation (ou l'écart
type relatif) de chacune des valeurs en entrée. Ceci nous permettra 
par la suite de comparer ces mêmes variables avec leurs valeurs en sortie. 

Nous avons obtenu les résultats suivants :

.. list-table:: Coefficients de variation des variables d'entrée
   :widths: 50 50
   :header-rows: 1

   * - Feature
     - Variation_coefficient %

   * - tgi
     - 4.35

   * - tvi 
     - 1.35  

   * - sfc
     - 0.84                   

   * - mass
     - 0.84                   

   * - drag
     - 0.84 

On remarque que le paramètre variant le plus est "tgi".

Sensibilité du vrai modèle aux incertitudes en entrée
------------------------------------------------------

On se permet dans un premier temps d'assembler un dataset en utilisant notre espace incertain
avec 30 évaluations de la fonction H2TurboFan.

Nous avons calculé certaines statistiques telles que la moyenne, l'écart-type et 
le coefficient de variation pour toutes les variables de ce dataset :

.. list-table:: Statistiques sur les variables du dataset assemblé à l'aide de l'espace incertain:
   :widths: 25 25 25 25
   :header-rows: 1


   * - Feature
     - Mean
     - std
     - Variation_coefficient %

   * - tgi
     - 0.28 
     - 0.12
     - 4.92 

   * - tvi 
     - 0.83 
     - 0.11 
     - 1.39  


   * - sfc
     - 1.01                   
     - 0.09 
     - 0.86 

   * - mass
     - 1.00                   
     - 0.09
     - 0.83

   * - drag
     - 1.01                    
     - 0.09
     - 0.89 

   * - mtow
     - 86978.95              
     - 44.76
     - 2.30


Les coefficients de variation des variables en entrée sont comparables à ceux calculés précedemment.
Le nombre de simulations de la fonction du modèle semble alors correct.

Sensibilité du métamodèle aux incertitudes en entrée
------------------------------------------------------

Par la suite, nous utilisons un métamodèle avec un régresseur linéaire pour assembler un deuxième dataset avec l'algorithme
de Monte Carlo.
Ce choix est justifié puisque la mesure d'apprentissage R2 de ce régresseur est de 0.997. Ce qui prouve que le surrogate model choisi
est une très bonne approximation du vrai modèle incertain.
Cette fois-ci nous nous permettons de faire 10000 simulations, puisque le surrogate model n'est pas
coûteux.

On obtient les résultats suivants:

.. list-table:: Statistiques sur les variables de sortie avec le métamodèle:
   :widths: 25 25 25 25
   :header-rows: 1


   * - Feature
     - Mean
     - std
     - Variation_coefficient %

   * - tgi
     - 0.29 
     - 0.11
     - 4.34

   * - tvi 
     - 0.83 
     - 0.11 
     - 1.35  


   * - sfc
     - 1.01                   
     - 0.09 
     - 0.84

   * - mass
     - 1.01                  
     - 0.09
     - 0.85

   * - drag
     - 1.01                    
     - 0.09
     - 0.85 

   * - mtow
     - 86812.50              
     - 40.85
     - 1.92

Les coefficients de variation des différentes variables d'entrée après assemblage du dataset avec le surrogate model
sont comparables à ceux calculés pour ces mêmes variables avant assemblage du dataset.

Pour une moyenne de coefficients de variance en entrée de 1.646, on obtient en sortie une valeur
moyenne de 1.92. Le modèle est donc peu sensible aux légères variations appliquées.

Analyse de sensibilité du modèle aux incertitudes : Indices de Sobol
---------------------------------------------------------------------
Nous commençons par assembler un dataset en utilisant l'espace incertain, 
et un algorithme de Monte Carlo en 30 simulations.

Ensuite nous créons un métamodèle de la fonction H2TurboFan avec un régresseur
linéaire. Ce choix à été justifié dans la partie précédente.

Ensuite nous lançons une analyse de Sobol sur le métamodèle avec 10000 simulations.
Le calcul des indices de Sobol pour les variables intervenant dans l'expression de 
la variable de sortie "mtow" donne les résultats suivants:

.. list-table:: Indices de sobol de 1er et 2ème ordre
   :widths: 40 30 30
   :header-rows: 1


   * - Indice Sobol'
     - 1er ordre
     - 2ème ordre
     
   * - drag
     - 0.91670406
     - 0.88685442

   * - mass
     - 0.02117337
     - 0.00250635

   * - sfc
     - 0.04620977
     - 0.04263135

   * - tgi
     - 0.0592
     - 0.03495691
    
   * - tvi
     - 0.0397296
     - 0.01243329

On remarque donc que la variable "drag" est celle qui contribue le plus à la variance de la variable "mtow"
que ce soit par son effet principale ou par ses interractions avec les autres variables.

Nous pouvons observer le même résultat sur la figure ci-dessous : 

.. figure:: ../_results/sobol_analysis.png
    :width: 50%

    Indices de Sobol


En conclusion, la variation des paramètres incertains a un impact relativement faible sur la fonction
objectif. Parmi ces paramètres, les indices de Sobol nous montrent que c'est le paramètre "drag" qui regroupe 
la quasi totalité de l'impact. 
