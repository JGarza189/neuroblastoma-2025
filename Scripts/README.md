## Scripts

This directory contains the core scripts for simulating and analyzing the tumor-immune interaction model in neuroblastoma. All scripts are intended to be used within a Jupyter Notebook environment.

### model.toml  
Defines the system of ordinary differential equations (ODEs) in both dimensional and nondimensional forms using TOML format. Used for structured parsing of model equations.

### model.txt  
Plain-text version of the ODE model structure. Functionally equivalent to `model.toml` but may be preferred for simpler parsing or legacy compatibility.

### modeling_utils.py  
Provides utility functions for parameter formatting, symbolic substitutions, drug dosing dynamics, and plotting. Supports model execution and analysis pipelines.

### parameters-mk04-nondimensional.txt  
Specifies nondimensionalized parameters and initial conditions. Enables analysis and simulation of the scaled version of the model.

### parameters-mk04.txt  
Contains dimensional parameter values, initial conditions, drug dosages, and symbolic substitutions. Parameters are sourced from literature and experimental data.

### run_model.py  
Primary simulation script that loads model equations and parameters, integrates the ODEs, and generates output plots for various treatment scenarios.

### stability_analysis.ipynb  
Jupyter Notebook for symbolic and numerical stability analysis. Includes Jacobian evaluation, equilibrium point analysis, and investigation of system behavior under perturbation.
