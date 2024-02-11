"""
Design of experiments
=====================

"""
from gemseo.api import configure_logger
from gemseo.api import create_design_space
from gemseo.api import create_discipline

# %%
# Create the discipline:
from gemseo.api import create_scenario

configure_logger()

discipline = create_discipline("AnalyticDiscipline",expressions={"z":"(1-x)**2+100*(y-x**2)**2"},name="Rosenbrock")

# %%
# Create the discipline:
design_space = create_design_space()
design_space.add_variable("x",l_b=-2,u_b=2)
design_space.add_variable("y",l_b=-2,u_b=2)

# %%
# Create the scenario:
scenario = create_scenario([discipline],"DisciplinaryOpt", "z", design_space, scenario_type="DOE")
scenario.execute({"algo": "OT_OPT_LHS", "n_samples": 100})

# %%
# Export the results to a dataset:
dataset = scenario.export_to_dataset(opt_naming=False)

# %%
# Export the dataset to a pandas dataframe:
df = dataset.export_to_dataframe()
print(df)

# %%
# .. seealso::
#
#    - `Dataset examples <https://gemseo.readthedocs.io/en/stable/examples/dataset/index.html>`__
#    - `DOE examples <https://gemseo.readthedocs.io/en/stable/examples/doe/index.html>`__
