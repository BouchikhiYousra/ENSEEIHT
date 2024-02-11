from setuptools import find_packages, setup

VERSION = '0.0.1' 
DESCRIPTION = 'h2_turbofan'
# LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="h2_turbofan", 
        version=VERSION,
        # author="Jason Dsouza",
        # author_email="<youremail@email.com>",
        description=DESCRIPTION,
        # long_description=LONG_DESCRIPTION,
        packages=find_packages("."),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
)
