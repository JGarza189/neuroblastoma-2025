## Parameter Selection

This document outlines the parameters used in our system of ordinary differential equations (ODEs) for modeling the interactions between cell populations $N$ (Natural Killer Cells), $L$ (CTL Cells), $T$ (Tumor Cells), whilst incorporating a drug interaction term $D$ (Drug Concentration). The model incorporates various tumor stages and treatment strategies, which are critical for defining initial conditions and simulating the progression of Neuroblastoma over time.

The interactions between tumor progression, drug concentration, and patient population drive the proposed initial conditions, which are tailored according to the patient's disease stage and patient profile. This modeling approach optimizes treatment plans by simulating various scenarios and predicting treatment efficacy for individual patient populations.

### Patient Populations

Our approach to modeling the immunotherapeutic dynamics of neuroblastoma is grounded in the International Neuroblastoma Risk Group (INRG) classification system. This risk stratification framework enhances comparability across clinical trials by categorizing patients based on tumor biology and disease stage. In this study, we derived a system to model patient populations based on the INRG system, enabling more robust cross-study comparisons and ensuring clinical relevance in our model design.

| **Risk Category**     | **INRG Stage(s)** | **Description**                                                                                                                                                                                                                     |
|-----------------------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Low Risk**          | L1, MS            | - **L1**: Localized tumor confined to one body compartment and not involving vital structures (no image-defined risk factors). <br> - **MS**: Metastatic disease in children <18 months with metastases limited to skin, liver, and/or bone marrow and favorable biology. These patients often require only observation or minimal intervention. |
| **Intermediate Risk** | L2, MS            | - **L2**: Locoregional tumor with one or more image-defined risk factors (IDRFs). <br> - **MS**: Patients with unfavorable biology (e.g., diploidy) are reclassified into intermediate risk. Treatment may involve chemotherapy and surgery when feasible. |
| **High Risk**         | M, MS, L2         | - **M**: Distant metastatic disease (excluding stage MS). <br> - **MS**: Cases with MYCN amplification are considered high risk regardless of age. <br> - **L2**: In patients over 18 months with unfavorable biological features. These patients require aggressive multimodal therapy including chemotherapy, surgery, and stem cell transplant. |


To establish the initial conditions for our mathematical model, we utilized three distinct patient populations—low-risk, intermediate-risk, and high-risk—based on tumor stage and biological factors. We then derived the relative initial abundance of tumor cells, CTLs, and NK cells for each patient population using data from published literature, ensuring that the initial conditions capture the clinical variability in immune cell populations across the different risk groups, with a particular emphasis on relative ratios. 

### Initial Conditions for Various Patient Populations

| **Parameter** | **Description**                       | **Unit** | **Low Risk** | **Intermediate Risk** | **High Risk** |
|---------------|----------------------------------------|----------|--------------|------------------------|---------------|
| **N₀**        | Initial amount of NK cells             | cells    |      -       |          -             |      -        |
| **L₀**        | Initial amount of CTL cells            | cells    |      -       |          -             |      -        |
| **T₀**        | Initial amount of tumor cells          | cells    |      -       |          -             |      -        |


The low-risk population is characterized by a relatively low tumor cell count and a robust immune response. Natural killer (NK) cells, part of the innate immune system, provide immediate defense, while cytotoxic T lymphocytes (CTLs) of the adaptive immune system offer targeted, long-term protection—though in lower abundance than NK cells. In intermediate-risk patients, a higher tumor burden prompts a more prominent role for CTLs. While NK cells remain the frontline defense, the growing tumor population necessitates a more coordinated immune response. In high-risk individuals, tumor cell counts are further elevated, posing greater challenges to immune control. CTLs become essential for sustained tumor suppression due to their antigen-specific targeting, while NK cells continue to provide rapid, nonspecific immune activity.

### Parameter Selection

In this section, we outline the key parameters that need to be defined based on existing literature to accurately model the immune-cellular dynamics of neuroblastoma progression. These parameters are crucial for setting up the system of ordinary differential equations and understanding the interactions between tumor cells, natural killer cells (NK), cytotoxic T lymphocytes (CTLs), and the impact of therapeutic agents such as IL-2 and Cyclophosphamide.
