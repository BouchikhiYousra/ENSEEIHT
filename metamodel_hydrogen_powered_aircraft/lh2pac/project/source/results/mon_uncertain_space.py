
"""
LH2pac Uncertain space
===============

Here we create an uncertain space by introducing some
uncertainties on the input variables of the LH2pac model
-------------------------

Firstly, we import the class ParameterSpace
"""
from gemseo.algos.parameter_space import ParameterSpace

# %%
# Create a class of uncertain space
# ---------------------------------

class lh2pacUncertainSpace(ParameterSpace):

    def __init__(self):
        super().__init__()
        self.add_random_variable(
            "tgi", "OTTriangularDistribution", minimum=0.25, mode=0.3, maximum=0.305
        )
        self.add_random_variable(
            "tvi", "OTTriangularDistribution", minimum=0.8, mode=0.845, maximum=0.85
        )
        self.add_random_variable(
            "sfc", "OTTriangularDistribution", minimum=0.99, mode=1., maximum=1.03 #propulsion
        )
        self.add_random_variable(
            "mass", "OTTriangularDistribution", minimum=0.99, mode=1., maximum=1.03 #structure
        )
        self.add_random_variable(
            "drag", "OTTriangularDistribution", minimum=0.99, mode=1., maximum=1.03  #aero
        )