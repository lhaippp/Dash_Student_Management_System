from jupyter_plotly_dash import JupyterDash

import plotly
import plotly.graph_objs as go
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from plotly import tools

plotly.offline.init_notebook_mode(connected=True)

group_by = 'num_groupe_etudiant'
reindex = True
ascending = False

colorscale = [[0, 'rgb(178, 10, 28)'],[1, 'rgb(129, 201, 159)']]
colorbar = {'lenmode':'pixels','len':200, 'yanchor':'top', 'y':1, 'dtick':1}

df_students = pd.read_csv('students.csv')
df_students.columns = [x.lower() for x in df_students.columns]
#df_students['niveau_atteint_max_francais'].fillna('Maternel', inplace=True)

group_variables = ['id_eleve','groupe_promo','num_groupe_etudiant','libelle','site',
                    'code_formation','code_admission','niveau_atteint_max_francais']
                    
df = pd.read_csv('fact_table_bi_exam.csv')
df.columns = [x.lower() for x in df.columns]

df_students.head()


app = JupyterDash('SimpleExample')

app.layout = html.Div([
    dcc.Dropdown(
        options=[{'label': i, 'value': i} for i in df_students.num_groupe_etudiant.unique()],
        id='dropdown'
    ),
    html.H3(id='output')
])

@app.callback(Output('output', 'children'), [Input('dropdown', 'value')])
def display_output(value):
    return str(value)

app
