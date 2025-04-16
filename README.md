## Tumor Progression and Pharmacological Intervention: Modeling Immunotherapeutic and Chemotherapy Strategies in Neuroblastoma

#### Project Contributors:  
Kate Brockman², Brian Colburn¹, Joseph Garza³, Tony Liao¹, BV Shankara Narayana Rao¹

#### Affiliations:
1. Department of Mathematics and Statistics, Texas A&M University - Corpus Christi  
3. Department of Engineering, Texas A&M University - Corpus Christi
2. Department of Life Sciences, Texas A&M University - Corpus Christi

##### **Keywords**: Mathematical Modeling; Tumor–Immune Interactions; Immunotherapy; Chemotherapy; Ordinary Differential Equations; Cancer Treatment Optimization

## Overview:
This repository contains scripts, data, and supplementary materials for an applied mathematical modeling project. The project focuses on developing a system of coupled first-order ordinary differential equations to model tumor-immune dynamics and assess the effects of immunotherapy and chemotherapy. Specifically, the model captures interactions between tumor cells, natural killer (NK) cells, cytotoxic T lymphocytes (CTLs), and therapeutic agents.

### Objectives

This project explored the role of immunotherapy and chemotherapy in suppressing tumor growth, focusing on how immune responses and treatment strategies influence tumor dynamics. The primary objectives are:

- **Objective 1**: Develop a system of ordinary differential equations to model interactions among natural killer (NK) cells, cytotoxic T lymphocytes (CTLs), and tumor cells.

- **Objective 2**: Evaluate the effects of immunotherapy and chemotherapy by simulating how therapeutic agents (e.g., IL-2 and Cyclophosphamide) modulate tumor growth and immune activation.

$$
\begin{aligned}
\begin{cases}
N'(t) = a_1 N(t)(1 - bN(t)) - a_2 N(t) - \alpha_1 N(t) T(t) + k_i I(t), \\
L'(t) = r_1 N(t) T(t) - \mu L(t) - \beta_1 L(t) T(t), \\
T'(t) = c T(t)(1 - d T(t)) - \alpha_2 N(t) T(t) - \beta_2 L(t) T(t) - k_c C(t), \\
I'(t) = -\frac{\log(2)}{h_i} 2^{-\frac{t}{h_i}} I(0), \\
C'(t) = -\frac{\log(2)}{h_c} 2^{-\frac{t}{h_c}} C(0).
\end{cases}
\end{aligned}
$$

This study integrates immunological and pharmacokinetic components to simulate tumor progression under varying treatment scenarios. The model aims to provide insight into how combination therapies can be optimized to improve clinical outcomes in neuroblastoma.
