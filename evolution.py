import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go

app = dash.Dash()

app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

df = pd.read_csv(
    'https://raw.githubusercontent.com/lhaippp/Dash_Student_Management_System/devs/Data/note_eleve.csv'
)

df['id_eleve']= df['id_eleve'].astype(str)
df['id_groupe']= df['id_groupe'].astype(str)
df['average'] = round(df.mean(numeric_only=True, axis=1),2)

df.rename(columns={'id_groupe':'Groupe','id_eleve':'Identificateur','name':'Élève','average':'Moyenne'},  inplace=True)


app.layout = html.Div([
    html.H4('Suivi des performances '),
    dt.DataTable(
        rows=df.to_dict('records'),
        # optional - sets the order of columns
        columns=['Identificateur','Élève','Groupe','Moyenne'],
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[0],
        editable=False,
        id='datatable-gapminder'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-gapminder'
    ),
], className="container")


@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    l = dff.iloc[selected_row_indices[0]][df.filter(like='qcm').columns].tolist()
    i=0
    moy=[]
    j=0
    s=0
    for i in range(len(l)):
        while (j<=i):
            s=s+l[j]
            j+=1
            moy.append(round(s/(j),2))
    
    fig = go.Figure(
        data=[
            go.Scatter(
            x=dff.filter(like='qcm').columns.tolist(),
            y=moy
            ),
            go.Bar(
            x= dff.filter(like='qcm').columns.tolist(),
            y= l,
            width = 0.5,
            marker=dict(
                    color='rgb(158,202,225)',
                    line=dict( color='rgb(8,48,107)', width=1.5,)
                    ),
            )],
            layout=go.Layout(
            title='Evolution de note par étudiant',
            showlegend=True,
            yaxis=dict(range=[0, 20]),
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
    )
    return fig


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=False)
