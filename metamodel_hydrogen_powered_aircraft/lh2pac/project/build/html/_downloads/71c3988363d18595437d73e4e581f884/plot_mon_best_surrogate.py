r"""
LH2pac Surrogate models
===============

In this example,
we will build a surrogate model for the H2TurboFan problem using
several Regressors. After comparing their R2 measures, 
we will optimize the best surrogate model.
"""
#%%
from gemseo.api import configure_logger
from gemseo.api import create_scenario
from gemseo.api import create_surrogate
from gemseo.mlearning.qual_measure.r2_measure import R2Measure
from gemseo_mlearning.api import sample_discipline
from discipline import H2TurboFan
from plot_mon_design_space import lh2pacDesignSpace
from marilib.utils import unit
import matplotlib.pyplot as plt
import pandas as pd

#%% We start by activating a logger
configure_logger()

# %%
# Firstly,
# we instantiate the H2TurboFan discipline
discipline = H2TurboFan()

# %%
# Then, we import the design space:
design_space = lh2pacDesignSpace()
print(design_space)

# %%
# Then,
# we sample the discipline with an optimal LHS:
dataset = sample_discipline(discipline, design_space, \
    output_names=["mtow","tofl","vapp", "vz_mcl","vz_mcr","oei_path","ttc","far"],\
        algo_name= "OT_OPT_LHS", n_samples= 30)

# %%
# We instantiate the dataframes that will be used to compare the different surrogate models :  
data_r2 = pd.DataFrame()
data_r2_kfold = pd.DataFrame()

# %%
# Creating a Linear Regressor surrogate model and computing the R2 measure : 
surrogate_discipline1 = create_surrogate("LinearRegressor", dataset)
r2 = R2Measure(surrogate_discipline1.regression_model, True)
data_r2['LinearReg'] =  r2.evaluate_learn()
data_r2_kfold['LinearReg'] =  r2.evaluate_kfolds()
print("r2 de l'evaluate_learn",data_r2['LinearReg'])  # learning measure
print("\n\n")
print("r2 de l'evaluate_kfolds",data_r2_kfold['LinearReg'])  # k-folds cross-validation measure
print("\n\n")

# %%
# Creating a Polynomial Regressor surrogate model and computing the R2 measure : 
surrogate_discipline1 = create_surrogate("PolynomialRegressor", dataset, degree = 3)
r2 = R2Measure(surrogate_discipline1.regression_model, True)
data_r2['PolyReg'] =  r2.evaluate_learn()
data_r2_kfold['PolyReg'] =  r2.evaluate_kfolds()
print("r2 de l'evaluate_learn",data_r2['PolyReg'])  # learning measure
print("\n\n")
print("r2 de l'evaluate_kfolds",data_r2_kfold['PolyReg'])  # k-folds cross-validation measure
print("\n\n")

# %%
# Creating a RBF Regressor surrogate model and computing the R2 measure : 
surrogate_discipline2 = create_surrogate("RBFRegressor", dataset)
r2 = R2Measure(surrogate_discipline2.regression_model, True)
data_r2['RBF'] =  r2.evaluate_learn()
data_r2_kfold['RBF'] =  r2.evaluate_kfolds()
print("r2 de l'evaluate_learn",data_r2['RBF'])  # learning measure
print("\n\n")
print("r2 de l'evaluate_kfolds",data_r2_kfold['RBF'])  # k-folds cross-validation measure
print("\n\n")

# %%
# Creating a Gaussian Process Regressor surrogate model and computing the R2 measure : 
surrogate_discipline3 = create_surrogate("GaussianProcessRegressor", dataset)
r2 = R2Measure(surrogate_discipline3.regression_model, True)
data_r2['GP'] =  r2.evaluate_learn()
data_r2_kfold['GP'] =  r2.evaluate_kfolds()
print("r2 de l'evaluate_learn",data_r2['GP'])  # learning measure
print("\n\n")
print("r2 de l'evaluate_kfolds",data_r2_kfold['GP'])  # k-folds cross-validation measure
print("\n\n")


# %%
# Let's compare the results of the differents models
labels=["mtow","tofl","vapp", "vz_mcl","vz_mcr","oei_path","ttc","far"]

fig = plt.figure(figsize=(6,3))
plt.plot(range(len(labels)),data_r2, '.', )
plt.xticks(range(len(labels)), labels, rotation = 'vertical')
plt.legend(['LinearRegressor', 'PolynomialRegressor', 'RBFRegressor', 'GaussianProcessRegressor'], \
    bbox_to_anchor=(1,1), loc="upper left")
fig.savefig('surrogate_r2.png', bbox_inches='tight', dpi=150)
plt.show()

fig = plt.figure(figsize=(5,4))
plt.plot(range(len(labels)),data_r2_kfold, '.', )
plt.xticks(range(len(labels)), labels, rotation = 'vertical')
plt.legend(['LinearRegressor', 'PolynomialRegressor', 'RBFRegressor', 'GaussianProcessRegressor'], \
    bbox_to_anchor=(1,1), loc="upper left")
plt.title("R2 Error on Kfolds")
fig.savefig('surrogate_r2_kfold.png', bbox_inches='tight', dpi=150)
plt.show()

# %%
#optimization of the best (based on the R2 results) surrogate model,
#Here it's the surrogate model created with a Gaussian Process Regressor 

#first we create a scenario
scenario = create_scenario([surrogate_discipline3], "DisciplinaryOpt", "mtow", design_space)
scenario.add_constraint("tofl", "ineq", positive=False, value = 2200.)
scenario.add_constraint("vapp", "ineq", positive=False, value = unit.mps_kt(137.))
scenario.add_constraint("vz_mcl", "ineq", positive=True, value = unit.mps_ftpmin(300.))
scenario.add_constraint("vz_mcr", "ineq", positive=True, value = unit.mps_ftpmin(0.))
scenario.add_constraint("oei_path", "ineq", positive=True, value=0.0011)
scenario.add_constraint("ttc", "ineq", positive=False, value=unit.s_min(25.)) 
scenario.add_constraint("far", "ineq", positive=False, value=13.4)

# %%
# before executing it with a gradient-free optimizer:
scenario.execute({"algo": "NLOPT_COBYLA", "max_iter": 1000})

# %%
# Lastly,
# we can plot the optimization history:
scenario.post_process("OptHistoryView", save=False, show=False, \
    file_path = "BestSurrogate")
plt.show()
