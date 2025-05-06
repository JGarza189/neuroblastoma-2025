from sympy import *
import sympy

from scipy.integrate import solve_ivp
import scipy.interpolate
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.gridspec
import seaborn as sns
import plotly.express as px

from pathlib import Path
import tomlkit

import IPython.display
from IPython.display import display, Markdown, Image

import modeling_utils
import numpy as np


NUM_DAYS = 6*21
#NUM_DAYS = 15


def mk_model(system, unknowns, params, drugs):

    model = Matrix([system[var].rhs
                    for var in unknowns
                    if var in system]
                  ).subs(params)
    
    display(Eq(Matrix([system[var].lhs
                       for var in unknowns
                       if var in system]), model))

    #drug_level_diffs = [total.derivative() for total in drugs]
    drug_level_diffs = [lambda _: 0 for total in drugs]
    
    lambdafied = lambdify(unknowns, model)
    
    def eval_model(t, y):
        return list(lambdafied(t, *y[:-2], *[levels(t) for levels in drugs])[:,0]) + [level(t) for level in drug_level_diffs]
    return eval_model


def main(model_path='model.txt', params_path='parameters-mk04.txt', args=None):
    args = args or []
    
    
    model_def = tomlkit.loads(Path(model_path).read_text())
    base_params = tomlkit.loads(Path(params_path).read_text())
    
    
    display(modeling_utils.params2df(base_params['parameters']).style.format('{:.4g}', subset='Value'))
    
    original_cases = list(base_params['initial_values'].items())
    
    #cases = cases[:1]
    
    cases = [
        (*case, cyclo_dose_vals['initial'], cyclo_dose_vals['recurring'], il2_dose_vals['recurring'], f'C: {cyclo_dose_name}, IL-2: {il2_dose_name}')
        for case in original_cases
        for il2_dose_name, il2_dose_vals in base_params['dosages']['I_2'].items()
        for cyclo_dose_name, cyclo_dose_vals in base_params['dosages']['C'].items()
    ]

    #print(original_cases)

    #original_cases = original_cases[2:3]

    if 'print_html' in args:
        for jx, (il2_dose_name, il2_dose_vals) in enumerate(base_params['dosages']['I_2'].items()):
            recurring_il2_dose = il2_dose_vals['recurring']

            #il2_header = f'''<p style="grid-column: {(ix+1)*3 + jx + 1} / span 1; grid-row: 2 / span 1;">IL-2: {il2_dose_name}</p>'''
            il2_header = f'''<p style="grid-column: {jx + 3} / span 1; grid-row: 1 / span 1;">IL-2: {il2_dose_name}</p>'''
            print(il2_header)

            for ix, case in enumerate(original_cases):
                risk_level = case[0]

                #risk_header = f'''<p style="grid-column: {(ix+1)*3 + 1} / span 3; grid-row: 1 / span 1;">{risk_level}</p>'''
                if jx == 0:
                    risk_header = f'''<p style="grid-column: 1 / span 1; grid-row: {(ix+1)*3 + 1} / span 3; writing-mode: sideways-lr; align-content: center;">{risk_level}</p>'''
                    print(risk_header)

                for kx, (cyclo_dose_name, cyclo_dose_vals) in enumerate(base_params['dosages']['C'].items()):
                    loading_cyclo_dose, recurring_cyclo_dose = cyclo_dose_vals['initial'], cyclo_dose_vals['recurring']
                    drug_label = f'C: {cyclo_dose_name}, IL-2: {il2_dose_name}'

                    if True or ix == 0:
                        cyclo_header = f'''<p style="grid-column: 2 / span 1; grid-row: {(ix+1)*3 + kx + 1} / span 1; writing-mode: sideways-lr; align-content: center;">Cyclo: {cyclo_dose_name}</p>'''
                        print(cyclo_header)

                    result_file = f'simulations/{risk_level}, {drug_label}.png'

                    sim_result = f'''<img style="grid-column: {jx + 3} / span 1; grid-row: {(ix+1)*3 + kx + 1} / span 1;" src="{result_file}"></img>'''
                    print(sim_result)

                    #print(f'{ix}, {jx}, {kx}, {risk_level}, {drug_label}')

    if 'no_sim' in args:
        return

    #model_type = 'basic'
    model_type = 'nondimensionalized'

    timescale = 1

    if model_type == 'nondimensionalized':
        timescale = base_params['parameters']['mu']['Value']
    
    for risk_level, ivs, loading_cyclo_dose, recurring_cyclo_dose, recurring_il2_dose, drug_label in cases:
        #if recurring_il2_dose == 0:
        #    continue
        concentrations = modeling_utils.mk_drug_concentration_table(11.23, NUM_DAYS, loading_cyclo_dose, recurring_cyclo_dose, recurring_il2_dose, timescale)
        il2 = scipy.interpolate.CubicSpline(concentrations.index, concentrations['Interleukin-2'])
        cyclo = scipy.interpolate.CubicSpline(concentrations.index, concentrations['Cyclophosphamide'])

        display(Markdown(f'# {risk_level}, {drug_label}'))
        print(loading_cyclo_dose, recurring_cyclo_dose)
        
        subs = ( modeling_utils.mk_subs_from_params(base_params['parameters'])
               | modeling_utils.mk_subs_from_params(ivs)
               #| {symbols('I_2'): il2, symbols('C'): cyclo}
               )

        for k, v in base_params['substitutions'].items():
            equation = sympify(v, {c: Function(c) for c in ivs.keys()})
            subs[k] = equation.subs(subs)
        
        display(modeling_utils.ivs2df(ivs).style.format('{:.1e}', subset='Value'))
        
        new_system = dict()
        
        for k, v in model_def[model_type].items():
            equation = sympify(v, {c: Function(c) for c in ivs.keys()})
            new_system[Function(k)(symbols('t'))] = Eq(symbols(k), equation)
            display(Eq(Function(k)(symbols('t')), equation))
            display(Eq(Function(k)(symbols('t')), equation.subs(subs)))
            #sympy.printing.tree.print_tree(equation, assumptions=False)

        
        model = mk_model(
            new_system,
            [symbols('t')] + [Function(c)(symbols('t')) for c in ivs.keys()],
            subs,
            [il2, cyclo],
            #[lambda t: 0, lambda t: 0],
        )
        
        #print([ivs['N'], ivs['L'], ivs['T'], ivs['D']])
        max_step_size = 1/60/24*timescale
        print(max_step_size)
        #end_step = NUM_DAYS*timescale
        end_step = 20*24*60*max_step_size
        print(end_step)
        sol = solve_ivp(model, [0, end_step], list(ivs.values()),
                        #method='DOP853',
                        #max_step=max_step_size
                       )
        df_1 = pd.DataFrame(
            {'days': sol.t
            } | {sym: sol.y[ix]
                               for ix, sym in enumerate(ivs.keys())}
        ).set_index('days')
        df_1['I_2'] = il2(df_1.index)
        df_1['C'] = cyclo(df_1.index)
        df_1.index = df_1.index/timescale

        #fig = modeling_utils.mk_subplots(df_1).update_layout(height=450, width=750)
        fig = modeling_utils.mk_subplots_no_drugs(df_1).update_layout(height=450/2, width=750)
        try:
            fig.write_image(f'simulations/{risk_level}, {drug_label}.png', format='png', scale=2)
            fig.write_html(f'simulations/{risk_level}, {drug_label}.html')
        except Exception as e:
            pass

        display(Image(data=fig.to_image(format='png', scale=2)))
        sns.lineplot(df_1.drop(columns=['I_2','C']))
        plt.yscale('log')

        #break


        """
        ax = sns.lineplot(df_1)
        display(ax)
        ax = None
        
        #fig, axes = plt.subplots(1, 5, figsize=(10,2))
        figsize=(8,6)
        fig = plt.figure(figsize=figsize)
        gs = matplotlib.gridspec.GridSpec(2,6, wspace=figsize[0]/11, hspace=0.375)
        grid_specs = [
            ((0,0), 2),
            ((0,2), 2),
            ((0,4), 2),
            ((1,0), 3),
            ((1,3), 3),
        ]
        for ix, col in enumerate(df_1.columns):
            position, width = grid_specs[ix]
            ax = fig.add_subplot(gs.new_subplotspec(position, colspan=width))
            sns.lineplot(df_1[col], ax=ax)
            ax.set_title(col)
            if ix == 0:
                ax.yaxis.set_label_text('cells')
            elif ix == 3:
                ax.yaxis.set_label_text('mg')
            else:
                ax.yaxis.label.set_visible(False)
            #if ix in [2]:
            #    ax.set_yscale('log')
        display(fig)
        """

if __name__ == '__main__':
    model_path = 'model.txt'
    params_path = 'parameters-mk04.txt'

    main(model_path, params_path)
