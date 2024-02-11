r"""
Optimization
============

some comment

"""
from gemseo.api import configure_logger
from gemseo.api import create_scenario

from discipline import H2TurboFan
from design_space import L2PACDesignSpace
from marilib.utils import unit

configure_logger()

discipline = H2TurboFan()

design_space = L2PACDesignSpace()

scenario = create_scenario([discipline],"DisciplinaryOpt", "mtow", design_space)
scenario.add_constraint("tofl", constraint_type="ineq", value=2200)
scenario.add_constraint("vapp", constraint_type="ineq", value=unit.mps_kt(137))
scenario.add_constraint(
    "vz_mcl", constraint_type="ineq", positive=True, value=unit.mps_ftpmin(300.0)
)
scenario.add_constraint(
    "vz_mcr", constraint_type="ineq", positive=True, value=unit.mps_ftpmin(0.0)
)
scenario.add_constraint(
    "oei_path", constraint_type="ineq", positive=True, value=1.1 / 100
)
scenario.add_constraint("ttc", constraint_type="ineq", value=unit.s_min(25))
scenario.add_constraint("far", constraint_type="ineq", value=13.4)

print(scenario)

scenario.execute({"algo": "NLOPT_COBYLA", "max_iter": 100})#, "algo_options": {"ftol_abs": 1e-4}

scenario.post_process("OptHistoryView", save=True, show=True)

