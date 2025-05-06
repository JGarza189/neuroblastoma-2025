## User-Guide

### Computer Set-up

To run simulations and reproduce the results presented in this study, use **Jupyter Notebook**, a graphical user interface that allows for interactive control of simulation parameters and real-time visualization of outputs. Alternatively, simulations may be executed through the **command line** using a shell terminal. 

## Required Software

Before getting started, ensure that Jupyter Notebook's interface is accessible on your system:

#### Software

- **Jupyter Notebook**  
- **Git** – for cloning the repository at the command line

#### Python Libraries

This project relies on the following Python libraries:

- `scipy` – solving ordinary differential equations  

## Directory & Dependency Set-up

### 1. Clone the Repository

To clone the repository using a **graphical interface**, navigate to the repository’s homepage on GitHub. Click the green **"Code"** dropdown button, then select **"Download ZIP"** to download the project as a compressed file. Once downloaded, extract the contents to your desired directory location.

To clone the repository using the **command-line interface (shell)**, run the following command in your terminal from your target directory:

```bash
git clone https://github.com/JGarza189/neuroblastoma-25.git
```

### 2. Dependency Installation

Brian’s instructions for downloading dependencies.

### 3. Library and Module Installation

Brian’s instructions for library and module installation.

## Running Simulations
To run simulations and reproduce the results presented in this study:

### 1. Open Jupyter Notebook

Using Jupyter Notebook, load all of the scripts and files into your ?? :

```
model.toml

model.txt

modeling_utils.py

run_model.py

parameters-mk04-nondimensional.txt

parameters-mk04.txt

stability_analysis.ipynb

```

Once loaded, run the python scripts in order. If desired, export the outputs manually to a `Desired/` directory.

Simulations generated include graphical outputs representing tumor and immune cell population dynamics over time under various treatment conditions.