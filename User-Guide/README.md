## User-Guide

### Computer Set-up

To run simulations and reproduce the results presented in this study, use **Jupyter Notebook**, a graphical user interface that allows for interactive control of simulation parameters and real-time visualization of outputs. Alternatively, simulations may be executed through the **command line** using a shell terminal. 

## Required Software

Before getting started, ensure that Jupyter Notebook is accessible on your system:

#### Software

- **Jupyter Notebook**  
- **Git** – for cloning the repository at the command line

#### Python Libraries

This project relies on the following Python libraries:

- **scipy** – Solves ordinary differential equations  

## File Set-up

### 1. Cloning & Downloading the Repository

To download the repository using a **graphical user interface**, navigate to the repository’s homepage on GitHub. Click the green **"Code"** dropdown button, then select **"Download ZIP"** to download the project as a compressed file. Once downloaded, extract the contents to your desired directory location on your computing system.

To clone the repository using the **command-line interface (shell)**, run the following command in your terminal from your target directory:

```bash
git clone https://github.com/JGarza189/neuroblastoma-25.git
```

## Running Simulations
To run simulations and reproduce the results presented in this study:

### 1. Open Jupyter Notebook

While in Jupyter Notebook, load all of the scripts and files into your working directory:

```
1. model.toml

2. model.txt

3. modeling_utils.py

4. run_model.py

5. parameters-mk04-nondimensional.txt

6. parameters-mk04.txt

7. stability_analysis.ipynb
```

### 2. Running the Scripts

Once loaded, run the provided scripts.

### 3. Saving Output

Once all of the simulations are completed, save the output to your desired directory on your computer.

Simulations generated include graphical outputs representing tumor and immune cell population dynamics over time under various treatment conditions.