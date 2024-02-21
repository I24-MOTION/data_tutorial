# I-24 MOTION basic data tutorial
##### Version: 1.0
##### Last updated: 2024-02-21


## Overview

This repository includes example Python notebooks that demonstrate iterative parsing of the large JSON files that make up the MOTION datasets, basic visualization of trajectories, and calculation of summary statistics of trajectories.

## Use agreement

Use of this software is subject to the license (BSD 3-clause) included in the code repository. The following terms also apply to the I-24 MOTION project's data and software.

1. You are free to use this software and data in academic and commercial work. 
2. I-24 MOTION datasets contain anonymous trajectories. Any activities to re-identify individuals in the dataset or activities that may cause harm to individuals in the dataset are prohibited.
3. When you use I-24 MOTION software and/or data in published academic work, you are required to include the following relevant citations. This allows us to aggregate statistics on the data use in publications:

I24-MOTION System:

> Gloudemans, D., Wang, Y., Ji, J., Zachár, G., Barbour, W., Hall, E., Cebelak, M., Smith, L. and Work, D.B., 2023. I-24 MOTION: An instrument for freeway traffic science. Transportation Research Part C: Emerging Technologies, 155, p.104311.

```
@article{gloudemans202324,
  title={I-24 MOTION: An instrument for freeway traffic science},
  author={Gloudemans, Derek and Wang, Yanbing and Ji, Junyi and Zach{\'a}r, Gergely and Barbour, William and Hall, Eric and Cebelak, Meredith and Smith, Lee and Work, Daniel B},
  journal={Transportation Research Part C: Emerging Technologies},
  volume={155},
  pages={104311},
  year={2023},
  publisher={Elsevier}
}
```

4. You are free to create and share derivative products as long as you maintain the terms above. 
5. The data and software is provided “As is.” We make no other warranties, express or implied, and hereby disclaim all implied warranties, including any warranty of merchantability and warranty of fitness for a particular purpose.

## Requirements

The requirements for running the code in this tutorial are as follows:
- Python 3.10
- Supporting Python libraries: Pandas, Numpy, Matplotlib, ijson, Jupyter-lab
- A `requirements.txt` file is provided for creating a new Python environment for the tutorial if you wish. This is the officially supported method for running the tutorial, since the code was validated on this exact set of dependency versions. The process for creating a new environment is below.


## Clean installation

Starting with a clean Python environment (i.e., through Conda or venv) with the correct Python version and dependencies is the officially supported method for running VT-tools. The instructions for doing so using the Anaconda Python distribution are as follows.

- Create a new environment with Python 3.10 (you can substitute "i24_tutorial" for your own name if you wish): `conda create -n i24_tutorial python=3.10`. 
- Activate the new environment (substitute "i24_tutorial" for your own name if you altered it): `conda activate i24_tutorial`. 
- Change directory to the i24_tutorial location: `cd [PATH_TO_TUTORIAL]`.
- Install Python library dependencies: `pip install -r requirements.txt`.
