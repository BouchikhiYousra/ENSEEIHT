r"""
LH2pac Sensitivity analysis
====================

In this example,
we will use the Sobol' analysis to quantify the sensitivity of the surrogate model
to the uncertainty introduced in its input parameters:
"""
from numpy import array
from gemseo.api import create_surrogate
from gemseo_mlearning.api import sample_discipline
import pprint
from gemseo.api import configure_logger
from discipline import H2TurboFan
from mon_uncertain_space import lh2pacUncertainSpace
from gemseo.uncertainty.sensitivity.sobol.analysis import SobolAnalysis
from matplotlib import pyplot as plt


# %%
# Firstly,
# we define the discipline computing the h2turbofan

discipline = H2TurboFan()

# %%
# Then,
# we instantiate the uncertain space:
uncertain_space = lh2pacUncertainSpace()

# %%
# Thirdly,
# we sample the discipline with a Monte Carlo algorithm:
dataset = sample_discipline(discipline, uncertain_space, output_names=["mtow"], algo_name="OT_MONTE_CARLO", n_samples=30)


# %%
# Then we create a surrogate discipline:
surrogate_discipline = create_surrogate("RBFRegressor", dataset)

# %%
# and use it for prediction:
surrogate_discipline.execute({"x": array([1.])})

# %%
# From that,
# we launch a Sobol' analysis with 10000 samples:
sobol = SobolAnalysis([surrogate_discipline], uncertain_space, 10000)
sobol.compute_indices()

# %%
# and print the results:
pprint.pprint(sobol.first_order_indices)
pprint.pprint(sobol.total_order_indices)

# %%
# We can also plot & visualize both first-order and total Sobol' indices:
sobol.plot("mtow", save=True, show=False)
plt.show()
