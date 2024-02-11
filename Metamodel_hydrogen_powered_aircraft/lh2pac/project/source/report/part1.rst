Métamodélisation et optimisation
===================================

Dans ce premier problème, des hypothèses sont faites sur les valeurs des paramètres techniques 
en 2030. L'objectif est alors d'optimiser le critère MTOW en fonction des valeurs de : 

* Engine maximum thrust (100 kN ≤ thrust ≤ 150 kN)
* Engine Bypass Ratio (BPR) (5 ≤ BPR ≤ 12 )
* Wing area (120 m² ≤ area ≤ 200 m²)
* Wing aspect ratio (7 ≤ ar ≤ 12)

en respectant la liste des contraintes :

* Take Off Field Length (TOFL ≤ 2200 m)
* Approach speed (VAPP ≤ 137 kt)
* Vertical speed MCL rating  (300 ft/min ≤ VZ_MCL)
* Vertical MCR rating  (0ft/min ≤ VZ_MCR)
* One engine inoperative climb path  (1.1% ≤ OEI_PATH)
* Time To Climb to cruise altitude  (TTC ≤ 25 min)
* Fuselage Aspect Ratio  (FAR ≤ 13.4)

Cependant la fonction (H2TurboFan), développée par l'ENAC,
permettant d'évaluer le critère MTOW est supposée être très coûteuse
et nous ne disposons que de 30 évalutions. 

L'objectif de cette partie est donc de construire un meta-modèle ("surrogate model") 
approximant la fonction H2TurboFan. Ce surrogate model est alors beaucoup moins coûteux à faire tourner
et peut être optimisé.

Si le surrogate model approxime bien la fonction H2TurboFan, les valeurs 
optimales obtenues pour le surrogate seront aussi des valeurs optimales
pour notre critère MTOW.

Optimisation de H2TurboFan 
--------------------------

En 30 itérations
^^^^^^^^^^^^^^^^

En réalité, ici la fonction H2TurboFan n'est pas très coûteuse. On peut alors 
optimiser dans un premier temps directement la véritable fonction, en 30 évaluations,
ou en 100 itérations. Le résultat de cette optimisation pourra par la suite servir de 
référence pour les résultats obtenus avec les surrogate models.

.. figure:: ../_results/H2TurboFan30_objective.png
    :width: 50%

    Fonction Objectif : H2TurboFan

.. figure:: ../_results/H2TurboFan30_variables.png
    :width: 60%

    Valeurs des variables à chaque itération
    
.. figure:: ../_results/H2TurboFan30_ineq_constraints.png
    :width: 80%

    Valeurs des contraintes à chaque itération

.. note::

   Au bout des 30 itérations, on a bien une décroissance de la fonction objectif maps pas de convergence en seulement 30 itérations.
   Le second graphique permet de visualiser les valeurs prisent par les paramètres de design (paramètres optimisés). 
   Ici, les trois premières variables se stabilisent au bout d'environ 20 itérations. 
   Cependant la variable 'aspect_ratio' varie toujours à la fin de l'optimisation.
   
   Enfin, le dernier graphique représente les valeurs des contraintes, en vert les contraintes respectées
   et en rouge les contraintes non respectées. 
   Ici les contraintes vz_mcl, ttc et far sont bien respectées. 
   Les contraintes vapp et oei_path prennent les valeurs limites (en blanc). 
   Cependant la contrainte sur tofl n'est pas respectée.

L'optimisation en 30 itérations de H2TurboFan ne converge pas. 
Ici la fonction n'étant pas coûteuse, on peut se permettre d'essayer 
l'optimisation avec 100 itérations. On peut noter l'intérêt d'utiliser des
métamodèles. Ils sont approximés en 30 évaluations de H2TurboFan, mais dont 
l'optimisation peut-être faite avec un grand nombre d'itérations.

En 100 itérations
^^^^^^^^^^^^^^^^^

.. figure:: ../_results/H2TurboFan100_objective.png
    :width: 50%

    Fonction Objectif : H2TurboFan

.. figure:: ../_results/H2TurboFan100_variables.png
    :width: 60%

    Valeurs des variables à chaque itération
    
.. figure:: ../_results/H2TurboFan100_ineq_constraints.png
    :width: 80%

    Valeurs des contraintes à chaque itération

.. note::
    En 100 itérations, on remarque que les résultats sont bien meilleurs, on a :  
    
    * convergence de la solution
    * stabilisation des valeurs des paramètres
    * stabilisation des contraintes.

    De plus, toutes les contraintes du problème sont bien respectées.

Ce résultat en 100 itérations, nous servira de référence pour la suite. 


Création d'un surrogate model
-----------------------------

En réalité, les fonctions d'évaluation tel que H2TurboFan sont très coûteuses. 
Dans un premier temps, nous allons utiliser
les 30 évaluations de la fonction H2TurboFan pour construire une approximation. 
On utilise un modèle de régression linéaire, régression polynomiale, régression RBF, régression par processus gaussien.


Comparaison de surrogate model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: ../_results/surrogate_r2_kfold.png
    :width: 70%

    Comparaison des surrogate models

.. note::
    On compare les mesures du R2 sur les K-folds pour choisir le meilleur modèle, 
    en s'assurant de ne pas faire d'over-fitting.
    Les résultats d'approximation varient d'un paramètre à l'autre.
    Le meilleur surrogate est obtenu avec le Gaussian Process Regressor.

Parmi les surrogate testés, la régression par Processus Gaussien est la plus
adaptée pour prendre en compte la complexité d'une fonction. Le surrogate construit
sera utilisé pour l'optimisation.


Résultats de l'optimisation sur le surrogate model
--------------------------------------------------

En comparaison avec l'optimisation de H2TurboFan, celle du surrogate 
est très rapide en temps de calcul. On obtient les résultats suivant : 

.. figure:: ../_results/BestSurrogate_objective.png
    :width: 50%

    Fonction Objectif : Surrogate model

.. figure:: ../_results/BestSurrogate_variables.png
    :width: 60%

    Valeurs des variables à chaque itération
    
.. figure:: ../_results/BestSurrogate_ineq_constraints.png
    :width: 80%

    Valeurs des contraintes à chaque itération

.. note::
    Malgré de légères instabilités au début de l'optimisation, 
    les résultats sont globalement similaires à l'optimisation de H2TurboFan.
    La fonction objectif converge vers la même valeur. 
    Concernant les contraintes, elles se sont stabilisées rapidement, 
    mise à part tofl, mais elles sont bien toutes satisfaites à la fin 
    de l'optimisation. 

    Il peut être surprenant qu'une valeur plus faible de la fonction
    objectif est atteinte au début de l'optimisation. Cependant, pour cette
    valeur, on remarque sur le 3ème graphe que les contraintes n'étaient 
    pas respectées.


En conclusion, l'optimisation du surrogate a bien permis 
d'obtenir de bien meilleurs résultats que celle de H2TurboFan
en 30 itérations. La résolution du problème est bien possible 
en respectant les 7 contraintes, on obtient un poids optimal d'environ 79000 kg.

Cependant, en réalité les valeurs des paramètres 
techniques en 2030 sont incertaines. On peut prendre en compte
ces incertitudes et observer les conséquences sur la fonction objectif.