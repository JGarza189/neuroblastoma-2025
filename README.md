## Tumor Progression and Pharmacological Intervention: Modeling Immunotherapeutic and Chemotherapy Strategies in Neuroblastoma

### Project Contributors:  
Kate Brockman², Brian Colburn¹, Joseph Garza³, Tony Liao¹, BV Shankara Narayana Rao¹

#### Affiliations:
1. Department of Mathematics and Statistics, Texas A&M University - Corpus Christi  
3. Department of Engineering, Texas A&M University - Corpus Christi
2. Department of Life Sciences, Texas A&M University - Corpus Christi

##### **Keywords**: Mathematical Modeling; Tumor–Immune Interactions; Immunotherapy; Chemotherapy; Ordinary Differential Equations

#### [Published Journal Article in *Nature*](https://www.nature.com/)

## Abstract
Neuroblastoma, the most common solid tumor causing cancer in infants, remains a leading cause of childhood cancer-related mortality. Despite advances in treatment, there is an ongoing need for more effective mathematical models and therapies to improve outcomes across neuroblastoma-specific patient populations. Immunotherapy and chemotherapy, particularly the use of Interleukin-2 (IL-2) and Cyclophosphamide, have shown promising therapeutic effects by enhancing immune responses and targeting cancer cells. Therefore, this study developed a coupled, nonlinear system of first-order differential equations to model the immune-cellular dynamics of neuroblastoma progression. The mathematical model captured the interactions between tumor cells, natural killer cells (NK), and cytotoxic T lymphocytes (CTLs), while exploring how IL-2 and Cyclophosphamide influenced these cell populations. The model investigated tumor population dynamics across various patient profiles, assessing the therapeutic impact of IL-2 and Cyclophosphamide. This studies approach supports the optimization of immunotherapy and chemotherapy strategies, providing actionable insights on how to improve clinical outcomes in neuroblastoma treatment.

## Repository Overview
This repository contains scripts, data, and supplementary materials for an applied modeling study. The project focused on developing a system of coupled first-order ordinary differential equations to model tumor-immune dynamics and assess the effects of immunotherapy and chemotherapy. Specifically, the model captured interactions between tumor cells, natural killer (NK) cells, cytotoxic T lymphocytes (CTLs), and therapeutic agents.

## Study Objectives

This project explored the role of immunotherapy and chemotherapy in suppressing tumor growth, focusing on how immune responses and treatment strategies influence tumor dynamics. The primary objectives are:

- **Objective 1**: Develop a system of ordinary coupled differential equations to model interactions among natural killer (NK) cells, cytotoxic T lymphocytes (CTLs), and tumor cells.

- **Objective 2**: Evaluate the effects of immunotherapy and chemotherapy on distinct patient populations by simulating how therapeutic agents (IL-2 and Cyclophosphamide) modulate tumor growth and immune activation.

This study integrated immunological and pharmacokinetic components to simulate tumor progression under varying treatment scenarios. The model aimed to provide insights into how combination therapies can be optimized to improve clinical outcomes in neuroblastoma.

## Computer Set-up

To run simulations and reproduce the results presented in this study, you can use the **Jupyter Notebook interface**, a graphical user interface (GUI) that allows for interactive control of simulation parameters and real-time visualization of outputs. Alternatively, simulations may be executed through the **command line interface (CLI)** for a more automated, script-based workflow.

### Required Software

Before getting started, ensure the following tools and libraries are installed on your system:

#### Software

- **Python 3.9 or higher**  
- **Jupyter Notebook**  
- **Git** – for cloning the repository and using the command line

#### Python Libraries

This project relies on the following Python libraries:

- `numpy` – numerical operations and arrays  
- `scipy` – solving ordinary differential equations  
- `pandas` – data manipulation and organization  

## Directory & Dependency Set-up

### 1. Clone the Repository

Either clone the repository directly from GitHub using the web interface, or use the following BASH command to clone it into your desired local directory:

```bash
git clone https://github.com/JGarza189/neuroblastoma-25.git
```

### 2. Download Dependencies

Brian’s instructions for downloading dependencies.

### 3. Library and Module Installation

Brian’s instructions for library and module installation.

## Running Simulations
To run simulations and reproduce the results presented in this study:

### 1. Navigate to the Cloned GitHub Repository in Jupyter Notebook

Using Jupyter Notebook, load the scripts into your environment in the following order:

```
1. Script 1

2. Script 2

3. Script 3

4. Script 4
```

Once loaded, run the python script in order. If desired, export the outputs manually to a `Desired/` directory.

Simulations generated include graphical outputs representing tumor and immune cell population dynamics over time under various treatment conditions.