r"""
LH2pac Optimization 100 iterations
============

We want to optimize our real model through a 100 iterations

"""
from gemseo.api import configure_logger
from discipline import H2TurboFan
from plot_mon_design_space import lh2pacDesignSpace
from gemseo.api import create_scenario
from matplotlib import pyplot as plt
from marilib.utils import unit

# %%
# Before starting,
# we activate the logger as an optimization process logs meaningful information.
configure_logger()

# %%
# Firstly,
# we define the discipline computing the h2turbofan
discipline = H2TurboFan()

# %%
# Then, we instantiate the design space:
design_space = lh2pacDesignSpace()
print(design_space)


# %%
# Thirdly,
# we put these elements together in a scenario

scenario = create_scenario([discipline], "DisciplinaryOpt", "mtow", design_space)
scenario.add_constraint("tofl", "ineq", positive=False, value = 2200.)
scenario.add_constraint("vapp", "ineq", positive=False, value = unit.mps_kt(137.))
scenario.add_constraint("vz_mcl", "ineq", positive=True, value = unit.mps_ftpmin(300.))
scenario.add_constraint("vz_mcr", "ineq", positive=True, value = unit.mps_ftpmin(0.))
scenario.add_constraint("oei_path", "ineq", positive=True, value=0.0011)
scenario.add_constraint("ttc", "ineq", positive=False, value=unit.s_min(25.)) 
scenario.add_constraint("far", "ineq", positive=False, value=13.4)


# %%
# before executing it with a gradient-free optimizer:
scenario.execute({"algo": "NLOPT_COBYLA", "max_iter": 100})


# %%
# Lastly,
# we can plot the optimization history:
scenario.post_process("OptHistoryView", save=False, show=False, \
    file_path = "H2TurboFan100")
plt.show()