r"""
LH2pac Surrogate model
===============

In this example,
we will build a surrogate model for the H2TurboFan problem using
a Gaussian Process Regressor, and some constraints related to 
the optimization of this model.
"""

#%%
from gemseo.api import create_scenario
from gemseo.api import create_surrogate
from gemseo.api import import_discipline
from gemseo.mlearning.qual_measure.r2_measure import R2Measure
from gemseo.mlearning.qual_measure.rmse_measure import RMSEMeasure
from gemseo_mlearning.api import sample_discipline
from discipline import H2TurboFan
from mon_design_space import lh2pacDesignSpace
from marilib.utils import unit
import matplotlib.pyplot as plt
from numpy import array

# %%
# Firstly,
# we instantiate the discipline

discipline = H2TurboFan()

# %%
# Then, we instantiate the design space:

design_space = lh2pacDesignSpace()
print(design_space)

# %%
# Then,
# we sample the discipline with an optimal LHS:
dataset = sample_discipline(discipline, design_space, output_names=["mtow","tofl","vapp", "vz_mcl","vz_mcr","oei_path","ttc","far"],algo_name= "OT_OPT_LHS", n_samples= 30)

# %%
# before creating a surrogate discipline:
surrogate_discipline = create_surrogate("GaussianProcessRegressor", dataset)
# %%
# and using it for prediction:
surrogate_discipline.execute({"x": array([1.])})
print(surrogate_discipline.cache.last_entry)

# %%
#optimization of the surrogate model

#first we create a scenario
scenario = create_scenario([discipline], "DisciplinaryOpt", "mtow", design_space)
scenario.add_constraint("tofl", "ineq", positive=False, value = 2200.)
scenario.add_constraint("vapp", "ineq", positive=False, value = unit.mps_kt(137.))
scenario.add_constraint("vz_mcl", "ineq", positive=True, value = unit.mps_ftpmin(300.)) #ftpmin_mps
scenario.add_constraint("vz_mcr", "ineq", positive=True, value = unit.mps_ftpmin(0.))
scenario.add_constraint("oei_path", "ineq", positive=True, value=0.0011)
scenario.add_constraint("ttc", "ineq", positive=False, value=unit.s_min(25.)) # min_s
scenario.add_constraint("far", "ineq", positive=False, value=13.4)

# %%
# before executing it with a gradient-free optimizer:
scenario.execute({"algo": "NLOPT_COBYLA", "max_iter": 30})

# %%
# Lastly,
# we can plot the optimization history:
scenario.post_process("OptHistoryView", save=True, show=True, file_path="opt_history_GP")
plt.show()

# %%
# The underlying regression model can also be assessed,
# with the R2 measure for instance:
r2 = R2Measure(surrogate_discipline.regression_model, True)
print("r2 de l'evaluate_learn",r2.evaluate_learn())  # learning measure
print("\n\n")
print("r2 de l'evaluate_kfolds",r2.evaluate_kfolds())  # k-folds cross-validation measure
print("\n\n")
# %%
# or with the root mean squared error:
rmse = RMSEMeasure(surrogate_discipline.regression_model, True)
print("rmse de evaluate_learn",rmse.evaluate_learn())
print("\n\n")
print("rmse de evaluate_kfolds",rmse.evaluate_kfolds())
print("\n\n")

surrogate_discipline.serialize("mon_surrogate.pkl")

discipline = import_discipline("mon_surrogate.pkl")
discipline.execute({"x": array([1.])})
print(discipline.get_output_data())


