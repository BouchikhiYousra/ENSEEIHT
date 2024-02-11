r"""
Sensitivity analysis
====================

In this example,
we will use the Sobol' analysis to quantify
the sensitivity of the output of the Ishigami function to its inputs:

.. math::
   f(x_1,x_2,x_3)=\sin(x_1)+7\sin(x_2)^2+0.1*x_3^4\sin(x_1)

where :math:`x_1,x_2,x_3\in[-\pi,\pi].
"""
import pprint

from gemseo.algos.parameter_space import ParameterSpace
from gemseo.api import create_discipline
from gemseo.uncertainty.sensitivity.sobol.analysis import SobolAnalysis
from matplotlib import pyplot as plt
from numpy import pi

# %%
# Firstly,
# we create the Ishigami function:
discipline = create_discipline(
    "AnalyticDiscipline",
    expressions={"y": "sin(x2)+7*sin(x1)**2+0.1*x3**4*sin(x2)"},
    name="Ishigami"
)

# %%
# Then,
# we define the uncertain space with uniform distributions:
uncertain_space = ParameterSpace()
for name in ["x1", "x2", "x3"]:
    uncertain_space.add_random_variable(
        name, "OTUniformDistribution", minimum=-pi, maximum=pi
    )

# %%
# From that,
# we launch a Sobol' analysis with 1000 samples:
sobol = SobolAnalysis([discipline], uncertain_space, 1000)
sobol.compute_indices()

# %%
# and print the results:
pprint.pprint(sobol.first_order_indices)
pprint.pprint(sobol.total_order_indices)

# %%
# We can also plot visualize both first-order and total Sobol' indices:
sobol.plot("y", save=False, show=False)
# Workaround for HTML rendering, instead of ``show=True``
plt.show()
