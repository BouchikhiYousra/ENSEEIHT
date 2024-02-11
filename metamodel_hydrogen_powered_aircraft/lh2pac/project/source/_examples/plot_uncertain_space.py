"""
Uncertain space
===============

GEMSEO does not offer an uncertain space but a :class:`.ParameterSpace`,
grouping both deterministic and uncertain variables.
This is a subclass of :class:`.DesignSpace`
with a method :meth:`~.ParameterSpace.add_random_variable`.

Create an uncertain space
-------------------------

Firstly, we import the API function :func:`create_parameter_space` and NumPy materials:
"""
from gemseo.algos.parameter_space import ParameterSpace
from gemseo.api import create_parameter_space
from numpy import array

# %%
# Then, we create an empty :class:`.ParameterSpace`:

uncertain_space = create_parameter_space()

# %%
# and add a first uncertain variable :math:`u`,
# following the standard Gaussian distribution
uncertain_space.add_random_variable("u", "OTNormalDistribution")

# %%
# .. note::
#    OT stands for OpenTURNS, the UQ library used for sampling.

# %%
# We can also add a second uncertain variable :math:`v`
# following the Gaussian distribution with mean 2 and standard deviation 0.5:
uncertain_space.add_random_variable("v", "OTNormalDistribution", mu=2, sigma=0.5)

# %%
# as well as a third uncertain variable :math:`w`
# following a triangular distribution:
uncertain_space.add_random_variable("z", "OTTriangularDistribution", minimum=-1., mode=0.5, maximum=1.)

# %%
# We can print this :class:`.ParameterSpace`:
print(uncertain_space)

# %%
# .. note::
#    The initial current value corresponds to the mean of the random variables.

# %%
# Create a class of uncertain space
# ---------------------------------
# If we want to use this uncertain space more than once,
# it can be more convenient and Pythonic to use the object-oriented paradigm
# and subclass :class:`.ParameterSpace`:


class MyUncertainSpace(ParameterSpace):

    def __init__(self):
        super().__init__()
        self.add_random_variable("u", "OTNormalDistribution")
        self.add_random_variable(
            "v", "OTNormalDistribution", mu=2, sigma=0.5
        )
        self.add_random_variable(
            "z", "OTTriangularDistribution", minimum=-1., mode=0.5, maximum=1.
        )


# %%
# Then,
# we only have to instantiate :class:`MyUncertainSpace`:
uncertain_space = MyUncertainSpace()
print(uncertain_space)
