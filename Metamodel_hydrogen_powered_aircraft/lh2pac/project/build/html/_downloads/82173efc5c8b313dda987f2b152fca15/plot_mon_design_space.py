"""
LH2pac Design space
============

Create a design space for the lh2pac
---------------------
"""
from gemseo.algos.design_space import DesignSpace

class lh2pacDesignSpace(DesignSpace):

    def __init__(self):
        super().__init__()
        self.add_variable("thrust", l_b=1e5, u_b=150000, value=125000)
        self.add_variable("bpr", l_b=5, u_b=12, value=8.5)
        self.add_variable("area", l_b=120, u_b=200, value=160)
        self.add_variable("aspect_ratio", l_b=7, u_b=12, value=9.5)

