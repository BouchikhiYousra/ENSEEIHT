"""
Using H2TurboFan
================
"""

from numpy import array

from discipline import H2TurboFan

# %%
# Instantiate the discipline:
disc = H2TurboFan()

# %%
# Execute the discipline with the default input values:
disc.execute()

# %%
# Print the local data (= input and output values):
print(disc.local_data)

# %%
# Execute the discipline with custom input values:
disc.execute({"thrust": array([125100.0]), "tgi": array([0.31])})
print(disc.local_data)

# %%
# Get the input and output data:
input_data = disc.get_input_data()
output_data = disc.get_output_data()
