from sympy.abc import *
from sympy import *
from sympy import S
import sympy
from sympy.physics.units.quantities import Quantity
from sympy.physics.units import day

from scipy.integrate import solve_ivp
import scipy.interpolate
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.subplots
import plotly.graph_objects as go

from pathlib import Path
import tomlkit

import IPython.display
from IPython.display import display, Markdown, Image

def units(expr):
    expr = simplify(expr)
    return abs(expr.subs({x: 1 for x in expr.args
                               if not x.has(Quantity)
                                  and x != -1}))

def import_params_from_clipboard_md():
    df = pd.read_clipboard().map(lambda x: x.strip()
                                        if type(x) == str
                                        else x)
    df.columns = [col.strip() for col in df.columns]
    
    params = (df['Parameter']
             .str.replace('₁', '_1')
             .str.replace('₂', '_2')
             .str.replace('α', '\\alpha')
             .str.replace('β', '\\beta')
             .str.replace('μ', '\\mu')
             .str.replace('I₀', 'D_0')
             .apply(lambda x: f'${x.strip()}$'))
    df['Parameter'] = params
    
    units = (df['Units']
             .str.replace('⁻¹', '^{-1}')
             .apply(lambda x: f'${x.strip()}$'))
    df['Units'] = units
    
    df = df.set_index('Parameter')
    
    return df

def ivs2df(initial_values):
    initial_values = pd.DataFrame([{'Parameter': f'${k}(0)$', 'Value': v} for k,v in initial_values.items()]).set_index('Parameter')
    initial_values['Units'] = '$cell$'
    initial_values['Description'] = 'Initial cell count'
    initial_values.loc['$I_2(0)$', 'Units'] = '$mg$'
    initial_values.loc['$I_2(0)$', 'Description'] = 'Initial drug dose'
    initial_values.loc['$C(0)$', 'Units'] = '$mg$'
    initial_values.loc['$C(0)$', 'Description'] = 'Initial drug dose'

    return initial_values

def params2df(params):
    latex_syms = [latex(sym, mode='inline') for sym in mk_subs_from_params(params).keys()]
    params = pd.DataFrame(params).transpose().rename_axis(index='Parameter')
    params.index = latex_syms

    return params


def import_case(path, variables):
    case = tomlkit.loads(Path(path).read_text())

    subs = mk_subs_from_case(case, variables)
    
    return {'case': case, 'subs': subs}


def mk_subs_from_case(case, variables):
    subs = dict()

    for ix, info in case['parameters'].items():
        if ix.startswith('$') and ix.endswith('$'):
            sym_name = ix.removeprefix('$').removesuffix('$')
            if '(0)' in sym_name:
                sym = Function(sym_name[0])(0)
            else:
                sym = symbols(sym_name, real=True, positive=True)
        elif ix in variables:
            sym = variables[ix]
            sym /= units(sym)
        else:
            raise RuntimeError(f'Unable to define substitution for "{ix}"')

        case['parameters'][ix]['latex'] = latex(sym, mode='inline')

        subs[sym] = info['Value']

    for function, value in case['initial_values'].items():
        sym = Function(function)(0)

        case['parameters'][ix]['latex'] = latex(sym, mode='inline')

        subs[sym] = value

    return subs


def mk_subs_from_params(params):
    subs = dict()

    for ix, info in params.items():
        sym = sympify(ix, {c: Function(c)(0) for c in ['N', 'L', 'T', 'D_n', 'D_t']})
        if type(info) is tomlkit.items.Table:
            subs[sym] = info['Value']
        else:
            subs[sym] = info

    return subs

    for ix, info in case['parameters'].items():
        if ix.startswith('$') and ix.endswith('$'):
            sym_name = ix.removeprefix('$').removesuffix('$')
            if '(0)' in sym_name:
                sym = Function(sym_name[0])(0)
            else:
                sym = symbols(sym_name, real=True, positive=True)
        elif ix in variables:
            sym = variables[ix]
            sym /= units(sym)
        else:
            raise RuntimeError(f'Unable to define substitution for "{ix}"')

        case['parameters'][ix]['latex'] = latex(sym, mode='inline')

        subs[sym] = info['Value']

    for function, value in case['initial_values'].items():
        sym = Function(function)(0)

        case['parameters'][ix]['latex'] = latex(sym, mode='inline')

        subs[sym] = value

    return subs


def mk_subs_from_df(df):
    subs = dict()
    for ix, row in df.iterrows():
        if ix.startswith('$') and ix.endswith('$'):
            sym_name = ix.removeprefix('$').removesuffix('$')
            if '(0)' in sym_name:
                sym = Function(sym_name[0])(0)
            else:
                sym = symbols(sym_name, real=True, positive=True)
        else:
            sym = globals()[ix]

        subs[sym] = row.Value
    return subs

def mk_html():
    IPython.display.HTML(pd.DataFrame([{'Parameter': latex(lhs, mode='inline'),
                                    'Definition': latex(rhs, mode="equation"),
                                  'Value': rhs.subs(_131 | {sympify('T(0)'): 2}).n(6)}
     for lhs, rhs in new_param_definitions.items()]).set_index('Parameter').transpose().to_html())


def mk_cyclo_total(halflife, loading_dose, recurring_dose):
    #loading_dose = loading_dose*mass # 40-50 mg/kg over 2-5 days
    loading_duration = 2
    #recurring_dose = recurring_dose*mass # 10-15 mg/kg every 7-10 days
    dose_period = 7
    last_dose = None
    max_levels = 0
    had_recurring_dose = False

    def calc_levels(day):
        nonlocal last_dose
        nonlocal max_levels
        nonlocal had_recurring_dose

        hour_of_day = day*24%24
        minute_of_hour = hour_of_day*60%60
        decay = 0
        levels = 0

        if day <= loading_duration:
            levels = loading_dose/loading_duration
            max_levels = levels
            last_dose = day
            had_recurring_dose = True
        elif (day-loading_duration)%dose_period < 1 and not had_recurring_dose:
            levels = recurring_dose
            max_levels = levels
            last_dose = day
            had_recurring_dose = True
        else:
            levels = max_levels*2**(-(day-last_dose)/halflife)

            if (day-loading_duration)%dose_period > 1:
                had_recurring_dose = False

        return levels
    return calc_levels


def mk_IL2_total(dose, halflife):
    #dose = 0.037*mass #0.037 mg/kg
    last_dose = None
    max_levels = 0
    print(dose)

    def IL2_total(day):
        nonlocal last_dose
        nonlocal max_levels
        hour_of_day = day*24%24
        minute_of_hour = hour_of_day*60%60
        decay = 0
        levels = 0

        #if last_dose is not None:
        #    decay = -dose*np.log(2)/(2**((day-last_dose)/halflife)*halflife)

        if 5 < day%14:
            levels = max_levels*2**(-((day-last_dose)*60*24)/halflife)
            #decay += -dose*np.log(2)/(2**((day-last_dose)/halflife)*halflife)
            #return decay
        elif hour_of_day%8 > 1:
            levels = max_levels*2**(-((day-last_dose)*60*24)/halflife)
            #decay += -dose*np.log(2)/(2**((minute_of_hour-(hour_of_day%8)*60-15)/halflife)*halflife)
            #return decay
        elif minute_of_hour > 15:
            levels = max_levels*2**(-((day-last_dose)*60*24)/halflife)
            #decay += -dose*np.log(2)/(2**((minute_of_hour-15)/halflife)*halflife)
            #return decay
        else:
            last_dose = day
            levels = dose*minute_of_hour/15
            max_levels = levels

        return levels
    return IL2_total


def mk_drug_concentration_table(mass, days, loading_cyclo_dose, recurring_cyclo_dose, recurring_il2_dose, timescale=1):
    IL2_total = mk_IL2_total(recurring_il2_dose, 5)
    cyclo_total = mk_cyclo_total(537/60/24, loading_cyclo_dose*mass, recurring_cyclo_dose*mass)
    
    concentrations = pd.concat([
        pd.Series({t: cyclo_total(t) for t in np.linspace(0,days,days*24*60*1+1)}).rename('Cyclophosphamide'),
        pd.Series({t: IL2_total(t) for t in np.linspace(0,days,days*24*60*1+1)}).rename('Interleukin-2'),
    ], axis=1).rename_axis('Day')

    concentrations.index = concentrations.index*timescale

    return concentrations

#def mk_drug_concentration_func(table_populator


def mk_subplots(df):
    fig = plotly.subplots.make_subplots(
        rows=2, cols=6,
        specs=[[{"colspan": 2}, None, {"colspan": 2}, None, {"colspan": 2}, None],
               [{"colspan": 3}, None, None, {"colspan": 3}, None, None]],
        subplot_titles=['N', 'L', 'T', 'IL-2', 'Cyclophosphamide'],
        horizontal_spacing=0.095,
        vertical_spacing=0.125,
        #print_grid=True,
    )
    fig.add_trace(go.Scatter(x=df.index, y=df['N'], mode='lines'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['L'], mode='lines'), row=1, col=3)
    fig.add_trace(go.Scatter(x=df.index, y=df['T'], mode='lines'), row=1, col=5)
    fig.add_trace(go.Scatter(x=df.index, y=df['I_2'], mode='lines'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['C'], mode='lines'), row=2, col=4)
    fig = (fig
      .update_layout(
          template='simple_white',
          margin_l=0,
          margin_r=0,
          margin_t=40,
          margin_b=0,
          showlegend=False,
      )
      .update_traces(row=1,col=1, line_color='#00aaff')
      .update_traces(row=1,col=3, line_color='green')
      .update_traces(row=1,col=5, line_color='orange')
      .update_traces(row=2,col=1, line_color='blue')
      .update_traces(row=2,col=4, line_color='purple')
      .update_yaxes(type="log", row=1, col=1)
      .update_yaxes(type="log", row=1, col=5)
      .update_yaxes(title_text="cells", row=1, col=1)
      .update_yaxes(title_text="IU", row=2, col=1)
      .update_yaxes(title_text="mg", row=2, col=4)
      .update_yaxes(exponentformat='power', row=1)
      .update_yaxes(exponentformat='power', row=2, col=1)
      .update_traces(line_width=2.25))
    return fig


def mk_subplots_no_drugs(df):
    fig = plotly.subplots.make_subplots(
        rows=1, cols=6,
        specs=[[{"colspan": 2}, None, {"colspan": 2}, None, {"colspan": 2}, None]],
        subplot_titles=['N', 'L', 'T'],
        horizontal_spacing=0.095,
        vertical_spacing=0.125,
        #print_grid=True,
    )
    fig.add_trace(go.Scatter(x=df.index, y=df['N'], mode='lines'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['L'], mode='lines'), row=1, col=3)
    fig.add_trace(go.Scatter(x=df.index, y=df['T'], mode='lines'), row=1, col=5)
    fig = (fig
      .update_layout(
          template='simple_white',
          margin_l=0,
          margin_r=0,
          margin_t=40,
          margin_b=0,
          showlegend=False,
      )
      .update_traces(row=1,col=1, line_color='#00aaff')
      .update_traces(row=1,col=3, line_color='green')
      .update_traces(row=1,col=5, line_color='orange')
      .update_yaxes(type="log", row=1, col=1)
      .update_yaxes(type="log", row=1, col=5)
      .update_yaxes(title_text="cells", row=1, col=1)
      .update_yaxes(exponentformat='power', row=1)
      .update_traces(line_width=2.25))
    return fig
