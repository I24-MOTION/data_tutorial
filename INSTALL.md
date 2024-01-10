# Overview

This installation will aid you to install the python environment and its packages, to run the tutorial. 

We recommend the use of `miniconda` as the python environment creation, in order to avoid polluting your existing python installation. To install miniconda (if you do not already have it) visit https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html

# Create a conda environment

```
conda create -y -n i24motion python=3.10
```
And activate your environment:
```
conda activate i24motion
```

# Install the prerequisite packages

```
pip install -r requirements.txt
```

You should now be ready to run the tutorial.
