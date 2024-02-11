"""
Design space
============

Create a design space
---------------------

Firstly, we import the API function :func:`create_design_space` and NumPy materials:
"""
from gemseo.algos.design_space import DesignSpace
from gemseo.api import create_design_space
from numpy import array

# %%
# Then, we create an empty :class:`.DesignSpace`:

design_space = create_design_space()

# %%
# and add a first design variable :math:`x` without bounds:
design_space.add_variable("x")

# %%
# We can also add a second design variable :math:`y` of dimension 2
# with a lower bound and a current value:
design_space.add_variable("y", size=2, l_b=0., value=array([0.5,0.75]))

# %%
# as well as a third design variable :math:`z`
# with both lower and upper bounds but without default value:
design_space.add_variable("z", l_b=-1., u_b=1.)

# %%
# We can print this :class:`.DesignSpace`:
print(design_space)

# %%
# Create a class of design space
# ------------------------------
# If we want to use this design space more than once,
# it can be more convenient and Pythonic to use the object-oriented paradigm
# and subclass :class:`.DesignSpace`:


class MyDesignSpace(DesignSpace):

    def __init__(self):
        super().__init__()
        self.add_variable("x")
        self.add_variable("y", size=2, l_b=0., value=array([0.5,0.75]))
        self.add_variable("z", l_b=-1., u_b=1.)


# %%
# Then,
# we only have to instantiate :class:`MyDesignSpace`:
design_space = MyDesignSpace()
print(design_space)
