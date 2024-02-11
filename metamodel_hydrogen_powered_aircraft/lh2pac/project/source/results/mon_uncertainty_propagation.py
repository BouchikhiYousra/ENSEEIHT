r"""
LH2pac Uncertainty propagation
=======================

In this section,
we will propagate uncertainties through a discipline
"""
# %%
# Packages import
from importlib.metadata import distribution
from numpy import array
from gemseo.api import create_surrogate
from gemseo_mlearning.api import sample_discipline
from discipline import H2TurboFan
from mon_uncertain_space import lh2pacUncertainSpace
from gemseo.uncertainty.api import create_statistics
from gemseo_mlearning.api import sample_discipline
from gemseo.mlearning.qual_measure.r2_measure import R2Measure
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


# %%
# In this first section we want to do some statistics on the dataset sampeled with the real model
# Firstly,
# we call the lh2pac uncertain space
uncertain_space = lh2pacUncertainSpace()

# %%
# We compute the variation coefficient of the input parameters so that we can compare
# it with the output parameters
names = ["tgi","tvi","sfc","mass","drag"]
dic = {}
print ("{:<8} {:<15}".format('Feature', 'Variation_coef %'))
for name in names:
    distribution = uncertain_space.distributions[name]
    print(name, "     ", distribution.standard_deviation / distribution.mean * 100)


# %%
# Then,
# we call the discipline H2TurboFan:
discipline = H2TurboFan()

# %%
# Thirdly,
# we sample the discipline with a Monte Carlo algorithm:
dataset = sample_discipline(discipline, uncertain_space, output_names=["mtow"], algo_name="OT_MONTE_CARLO", n_samples=30)


# %%
# Lastly,
# we create a statistics object to estimate statistics,
# such as mean, variance and variation coefficient:
statistics = create_statistics(dataset)
mean = statistics.compute_mean()
variance = statistics.compute_standard_deviation()
cv = statistics.compute_variation_coefficient()
names = ["tgi","tvi","sfc","mass","drag", "mtow"]
print ("{:<8} {:<15} {:<10} {:<10}".format('Feature','Mean','std','Variation_coefficient %'))
for name in names:
    print("{:<8} {:<15} {:<10} {:<10}".format(name, "{:.2f}".format(mean[name][0]),\
         "{:.2f}".format(np.sqrt(variance[name][0])),"{:.2f}".format(cv[name][0]*100)))

# %%
# We can also plot the histogram of the variables in the dataset:
fig, axes = plt.subplots(2, 3)
for i in range(2):
    for ax, name in zip(axes[i], names):
        ax.hist(dataset[name])
        ax.set_title(name)
plt.show()


# %%
# In this second section we want to do some statistics on the dataset sampeled with the surrogate model
# so we can compare them with those of the dataset made with our true model 
surrogate_discipline = create_surrogate("LinearRegressor", dataset)
r2 = R2Measure(surrogate_discipline.regression_model, True)
print("R2: learning measure = \n", r2.evaluate_learn())  # learning measure
print("R2: k-folds cross-validation measure = \n", r2.evaluate_kfolds())  # k-folds cross-validation measure
#The learning measure equals to 0.997, hence the linear regression is a good fit for the surrogate model.

surrogate_dataset = sample_discipline(surrogate_discipline, uncertain_space, output_names=["mtow"], algo_name="OT_MONTE_CARLO", n_samples=30)

# %%
# Lastly,
# we create an :class:`.EmpiricalStatistics` object to estimate statistics,
# such as mean and variance:
surrogate_statistics = create_statistics(surrogate_dataset)
s_mean = surrogate_statistics.compute_mean()
s_variance = surrogate_statistics.compute_standard_deviation()
s_cv = surrogate_statistics.compute_variation_coefficient()
names = ["tgi","tvi","sfc","mass","drag", "mtow"]
print ("{:<8} {:<15} {:<10} {:<10}".format('Feature','Mean','std','Variation_coefficient %'))
for name in names:
    print("{:<8} {:<15} {:<10} {:<10}".format(name, "{:.2f}".format(s_mean[name][0]),\
         "{:.2f}".format(np.sqrt(s_variance[name][0])),"{:.2f}".format(s_cv[name][0]*100)))


# %%
# We can also plot the histogram of the variables in the surrogate_dataset:
fig, axes = plt.subplots(2, 3)
for i in range(2):
    for ax, name in zip(axes[i], names):
        ax.hist(surrogate_dataset[name])
        ax.set_title(name)
plt.show()


