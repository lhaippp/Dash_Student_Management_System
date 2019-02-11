# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

#Could be better if use a fact table instead?
df1 = pd.read_csv('note_eleve.csv')
df2 = pd.read_csv('eleve.csv')
df3 = pd.read_csv('ExportElevesUVSimple.csv')

#Dataframe modifications for the requirements
df2 = df2.merge(df3[['ID_ELEVE','groupe_promo', 'site', 'CODE_FORMATION']], left_on='id_eleve', right_on='ID_ELEVE').drop('ID_ELEVE',1)
df2.loc[df2['groupe_promo'] == 1, 'professor_name'] = 'Laurent'
df2.loc[df2['groupe_promo'] == 2, 'professor_name'] = 'Sylvie'
filter_col = [col for col in df1 if col.startswith('qcm')]
filter_col.sort()
df1['Avg'] = df1[filter_col].mean(axis=1).round(2)
filter_col.extend(['Avg','id_eleve'])
df2 = df2.merge(df1[filter_col], on='id_eleve')

#Better use a def with group_by?
df4 = df2.groupby(['niveau_initial_francais', 'niveau_atteint_francais'])['Avg'].mean().round(2).reset_index()
df5 = df2.groupby(['CODE_FORMATION'])['Avg'].mean().round(2).reset_index()
df6 = df2.groupby(['site'])['Avg'].mean().round(2).reset_index()
df7 = df2.groupby(['professor_name'])['Avg'].mean().round(2).reset_index()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Also, could use a def to plot these Bar charts?
trace1 = go.Bar(
    x = df4.iloc[:,0].map(str) + "_to_" + df4.iloc[:,1],
    y = df4.iloc[:,2],
    name = 'Average score per French level',
    showlegend = False
) 

trace2 = go.Bar(
    x = df5.iloc[:,0],
    y = df5.iloc[:,1],
    name = 'Average score per formation',
    showlegend = False
) 

trace3 = go.Bar(
    x = df6.iloc[:,0],
    y = df6.iloc[:,1],
    name = 'Average score per site',
    showlegend = False
) 

trace4 = go.Bar(
    x = df7.iloc[:,0],
    y = df7.iloc[:,1],
    name = 'Average score per professor',
    showlegend = False
)  

#Global average value, shown as a threshold line
trace5 = go.Scatter(
    x = [" "],    
    y = [df1['Avg'].mean()],
    mode = 'text',
    text = ['Global average'],
    name = 'Global average',
    showlegend = False
) 

#Tabs look nice :D. Need improvements though...   
app.layout = html.Div([
    html.H1('Professor view'),
    dcc.Tabs(id="tabs", value='tab_1', children=[
        dcc.Tab(label='French level', value='tab_1'),
        dcc.Tab(label='Formation', value='tab_2'),
        dcc.Tab(label='Site', value='tab_3'),
        dcc.Tab(label='Professor', value='tab_4'),
    ]),
    html.Div(id='tabs_content')    
    
]) 
@app.callback(Output('tabs_content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab_1':
        return html.Div([
            dcc.Graph(
                id='avg-tbl1',
                figure={
                    'data' : [trace1, trace5],
                    'layout' : {
                        'shapes' : [{
                            'type' : 'line',
                            'xref' : 'paper',
                            'yref' : 'y',
                            'x0' : 0,
                            'y0' : df1['Avg'].mean(),
                            'x1' : 1,
                            'y1' : df1['Avg'].mean(),
                            'line' : {
                                'color' : 'rgb(50, 171, 96)',
                                'width' : 3,
                                'dash' : 'dashdot'
                            },
                            'name' : 'Global average'
                        }],
                        'title' : 'Average score per French level',
                        'xaxis' : {
                            'title' : 'French level'
                        },
                        'yaxis' : {
                            'title' : 'Average score'
                        },       
                    }
                }
            )
        ])
    elif tab == 'tab_2':
        return html.Div([
            dcc.Graph(
                id='avg-tbl2',
                figure={
                    'data' : [trace2, trace5],
                    'layout' : {
                        'shapes' : [{
                            'type' : 'line',
                            'xref' : 'paper',
                            'yref' : 'y',
                            'x0' : 0,
                            'y0' : df1['Avg'].mean(),
                            'x1' : 1,
                            'y1' : df1['Avg'].mean(),
                            'line' : {
                                'color' : 'rgb(50, 171, 96)',
                                'width' : 3,
                                'dash' : 'dashdot'
                            },
                            'name' : 'Global average'
                        }],
                        'title' : 'Average score per formation',
                        'xaxis' : {
                            'title' : 'Formation'
                        },
                        'yaxis' : {
                            'title' : 'Average score'
                        },       
                    }
                }
            )
        ])
    elif tab == 'tab_3':
        return html.Div([
            dcc.Graph(
                id='avg-tbl3',
                figure={
                    'data' : [trace3, trace5],
                    'layout' : {
                        'shapes' : [{
                            'type' : 'line',
                            'xref' : 'paper',
                            'yref' : 'y',
                            'x0' : 0,
                            'y0' : df1['Avg'].mean(),
                            'x1' : 1,
                            'y1' : df1['Avg'].mean(),
                            'line' : {
                                'color' : 'rgb(50, 171, 96)',
                                'width' : 3,
                                'dash' : 'dashdot'
                            },
                            'name' : 'Global average'
                        }],
                        'title' : 'Average score per site',
                        'xaxis' : {
                            'title' : 'Site'
                        },
                        'yaxis' : {
                            'title' : 'Average score'
                        },       
                    }
                }
            )
        ])       
    elif tab == 'tab_4':
        return html.Div([
            dcc.Graph(
                id='avg-tbl4',
                figure={
                    'data' : [trace4, trace5],
                    'layout' : {
                        'shapes' : [{
                            'type' : 'line',
                            'xref' : 'paper',
                            'yref' : 'y',
                            'x0' : 0,
                            'y0' : df1['Avg'].mean(),
                            'x1' : 1,
                            'y1' : df1['Avg'].mean(),
                            'line' : {
                                'color' : 'rgb(50, 171, 96)',
                                'width' : 3,
                                'dash' : 'dashdot'
                            },
                            'name' : 'Global average'
                        }],
                        'title' : 'Average score per professor',
                        'xaxis' : {
                            'title' : 'Professor'
                        },
                        'yaxis' : {
                            'title' : 'Average score'
                        },       
                    }
                }
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=False)