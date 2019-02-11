import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import dash_table
import plotly.plotly as py
from dashboard_prof import dashboard_prof 
import dash_table_experiments as dt

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4',
        'crossorigin': 'anonymous'
    }
]

external_scripts = [
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/solid.js',
        'integrity': 'sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js',
        'integrity': 'sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://code.jquery.com/jquery-3.3.1.slim.min.js',
        'integrity': 'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js',
        'integrity': 'sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js',
        'integrity': 'sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm',
        'crossorigin': 'anonymous'
    }
]


dashboard = dashboard_prof('https://raw.githubusercontent.com/lhaippp/Dash_Student_Management_System/devs/Data')
url_fait = 'https://raw.githubusercontent.com/lhaippp/Dash_Student_Management_System/devs/Data/fact_table_bi_exam.csv'
df_fait = pd.read_csv(url_fait,index_col=0,parse_dates=[0])

url_student = 'https://raw.githubusercontent.com/lhaippp/Dash_Student_Management_System/devs/Data/eleve.csv'
df_students = pd.read_csv(url_student,index_col=0,parse_dates=[0])


df_students.columns = [x.lower() for x in df_students.columns]
df_students = df_students.sort_index(by = 'id_groupe', ascending= True)

group_variables = ['nom','prenom','id_groupe','niveau_initial_francais','niveau_atteint_francais']

df_students.niveau_atteint_francais[df_students.niveau_atteint_francais == '0']='Maternel'
df_students.niveau_initial_francais[df_students.niveau_initial_francais == '0']='Maternel'

app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets)

app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body id="page-top">
    <nav class="navbar navbar-expand navbar-dark bg-dark static-top">
      <button class="btn btn-link btn-sm text-white order-1 order-sm-0" id="sidebarToggle" href="#">
       <a class="navbar-brand mr-1" href="">  Analyse et suivi de l'acquisition des connaissances des étudiants (BI)</a>
        <i class="fas fa-bars"></i>
      </button>
    </nav>
    <div id="wrapper">
      <!-- Sidebar -->
      <ul class="sidebar navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="/page-1">
            <i class="fas fa-fw fa-tachometer-alt"></i>
            <span>Dashboard</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/page-2">
            <i class="fas fa-fw fa-chart-area"></i>
            <span>Evolution</span></a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/page-3">
            <i class="fas fa-fw fa-table"></i>
            <span>Profils</span></a>
        </li>
      </ul>
    <!-- /#wrapper -->
    
     {%app_entry%}
     {%config%}
     {%scripts%}
    <!-- Bootstrap core JavaScript-->
    <script src="vendor/jquery/jquery.min.js"></script>
    <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
    <!-- Core plugin JavaScript-->
    <script src="vendor/jquery-easing/jquery.easing.min.js"></script>
  </body>
</html>''' 
# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={'marginBottom': 50, 'marginTop': 25, 'marginLeft':25 })
])


index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go to Page 3', href='/page-3'),
])

page_1_layout = html.Div(children=[
    
    # html.H1('Page 1'),
    # dcc.Link('Go to Page 2', href='/page-2'),
    # html.Br(),
    # dcc.Link('Go back to home', href='/'),
    html.H1(children='Aperçu général des performances'),
    html.Div(children='''
        Veuillez choisir un Groupe
    '''),
   dcc.Dropdown(
        options=[{'label': 'Groupe ' + str(i), 'value': i} for i in df_students.id_groupe.unique()],
        id='dropdown',
        value='1',
        placeholder="Tous les groupes",
    ),
           html.Div(children='''
        Veuillez choisir une catégorie d'enseignement
    '''),
    dcc.Dropdown(
        options=[{'label': str(i), 'value': i} for i in df_fait.categorie.unique()],
        id='dropdown_categorie',
        placeholder="Toutes les catégories",
    ),
           
           
    html.H3(id='output'),
    
    html.Div(id='heatmap_div'),
    
    html.Div(id='graph_div'),
    
    # dcc.Graph(
    #  figure=go.Figure(
    #   data = [go.Scatterpolar(
    #   r = [39, 28, 8, 7, 28, 39],
    #   theta = [i for i in df_fait.categorie.unique().tolist()],
    #   fill = 'toself'
    #   )],
    
    #   layout = go.Layout(
    #   polar = dict(
    #   radialaxis = dict(
    #   visible = True,
    #   range = [0, 50])),
    #   showlegend = False
    #   )
    #  )
    # ),
    
    html.Div(id='table_div', style={'width': '1000px'})
    


])

@app.callback(Output('output', 'children'), [Input('dropdown', 'value')])
def display_output(value):
    return 'Visualisation des résultats pour Groupe '+str(value)

@app.callback(Output('table_div', 'children'), [Input('dropdown', 'value')])
def update_table(value):
    return  dt.DataTable(
            rows=df_students.loc[(df_students["id_groupe"]==value),].to_dict("rows"),
            columns=df_students.columns.tolist(),
            filterable=True,
            sortable=True,
            editable=False
            ),
            
@app.callback(Output('graph_div', 'children'), [Input('dropdown', 'value')])
def update_graph(id_groupe):
    df = dashboard.df_score(id_groupe)
    xticks = df['nom'].str.cat(df['prenom'],sep=' ').values.tolist()
    return dcc.Graph(
    figure=go.Figure(
        data=[
            go.Bar(
                x=xticks,
                y=df.reponse_correcte.values.tolist(),
                name='Réponses correctes',
                marker=go.bar.Marker(
                    color='rgb(97, 145, 1)'
                )
            ),
            go.Bar(
                x=xticks,
                y=df.reponse_fause.values.tolist(),
                name='Réponses incorrectes',
                marker=go.bar.Marker(
                    color='rgb(168, 4, 2)'
                )
            ),
            go.Bar(
                x=xticks,
                y=df.pas_de_reponse.values.tolist(),
                name='Pas de réponses',
                marker=go.bar.Marker(
                    color='rgb(136, 136, 136)'
                )
            )
        ],
        layout=go.Layout(
            title='Réponses au QCM par étudiant',
            showlegend=True,
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
        )
    ),
    style={'height': 400,'width':800}
    ),
      
        
@app.callback(Output('heatmap_div', 'children'), [Input('dropdown', 'value'),Input('dropdown_categorie', 'value')])
def update_heatmap(id_groupe,categorie):
    
    df = dashboard.df_heatmap(id_groupe,categorie)
    mx = dashboard.absence_matrix(id_groupe,categorie).iloc[:,4:].values
    mx2 = [['Reponses Correctes/ Questions repondu :'+mx[i,j] for j in range(len(mx[i]))]for i in range(len(mx))]
    
    yticks = df['nom'].str.cat(df['prenom'],sep=' ').values.tolist()
    xticks = [x for x in df.columns if x not in ['id_groupe','id_eleve','nom','prenom']]
    
    layout = go.Layout(
        autosize=False,
        width=300+50*len(xticks),
        height=100*len(yticks),
        margin=go.layout.Margin(
            l=150,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        xaxis=dict(
            title = 'categorie / sous-categorie',
            showticklabels=True,
            tickangle=15,
            tickfont=dict(
                #size=20,
                color='black'
            )
        ),
        yaxis=dict(
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                #size=20,
                color='black'
            )
        ),
        title='Evaluation Par Groupe',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff'
    )
    
    yticks = df['nom'].str.cat(df['prenom'],sep=' ').values.tolist()
    xticks = [x for x in df.columns if x not in ['id_groupe','id_eleve','nom','prenom']]
    trace = go.Heatmap(z=df[[x for x in df.columns if x not in ['id_groupe','id_eleve','nom','prenom']]].values,
                       y=yticks, ytype='array',
                       x= xticks, xtype='array',
                       zmin=0,zmax=1,
                       colorscale = [[0,'#a80101'],[0.5,"#dbf287"],[1,"#619101"]],
                       colorbar = dict(
                                    title = 'Percentage de correction',
                                    titleside = 'top',
                                    tickmode = 'array',
                                    tickvals = [0,0.5,1],
                                    ticktext = ['0%','50% ','100%'],
                                    ticks = 'outside'
                       ),
    #                    connectgaps= False
                       xgap=1,
                       ygap=5,
                       text=mx2,
                       hoverinfo = 'all'
                      )
    data=[trace]
    fig = go.Figure(data=data, layout=layout)
    return dcc.Graph(figure = fig )

# for the second page

df = pd.read_csv(
    'https://raw.githubusercontent.com/lhaippp/Dash_Student_Management_System/devs/Data/note_eleve.csv'
)

df['id_eleve']= df['id_eleve'].astype(str)
df['id_groupe']= df['id_groupe'].astype(str)
df['average'] = round(df.mean(numeric_only=True, axis=1),2)

df.rename(columns={'id_groupe':'Groupe','id_eleve':'Identificateur','name':'Élève','average':'Moyenne'},  inplace=True)


page_2_layout = html.Div([
    # html.H1('Page 2'),
    # html.Div(id='page-2-content'),
    # html.Br(),
    # dcc.Link('Go to Page 1', href='/page-1'),
    # html.Br(),
    # dcc.Link('Go back to home', href='/'),
    html.H1('Suivi des performances ', style={'width': '1000px'}),
    html.Div(children='''
        Veuillez sélectionner un Étudiant
    '''),
    
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


@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

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
            y=moy,
            name='Moyenne'
            ),
            go.Bar(
            x= dff.filter(like='qcm').columns.tolist(),
            y= l,
            width = 0.5,
            marker=dict(
                    color='rgb(158,202,225)',
                    line=dict( color='rgb(8,48,107)', width=1.5,)
                    ),
            name='Note'
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

# the third page

#Could be better if use a fact table instead?
df1 = pd.read_csv('Data/note_eleve.csv')
df2 = pd.read_csv('Data/eleve.csv')
df3 = pd.read_csv('Data/ExportElevesUVSimple.csv')

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
df2.niveau_atteint_francais[df2.niveau_atteint_francais == '0']='Maternel'
df2.niveau_initial_francais[df2.niveau_initial_francais == '0']='Maternel'
df4 = df2.groupby(['niveau_initial_francais', 'niveau_atteint_francais'])['Avg'].mean().round(2).reset_index()
df5 = df2.groupby(['CODE_FORMATION'])['Avg'].mean().round(2).reset_index()
df6 = df2.groupby(['site'])['Avg'].mean().round(2).reset_index()
df7 = df2.groupby(['professor_name'])['Avg'].mean().round(2).reset_index()

#Also, could use a def to plot these Bar charts?
trace1 = go.Bar(
    x = df4.iloc[:,0].map(str),
    y = df4.iloc[:,2],
    name = 'Note moyenne par niveau de français',
    showlegend = False
) 

trace2 = go.Bar(
    x = df5.iloc[:,0],
    y = df5.iloc[:,1],
    name = 'Note moyenne par formation',
    showlegend = False
) 

trace3 = go.Bar(
    x = df6.iloc[:,0],
    y = df6.iloc[:,1],
    name = 'Note moyenne par site',
    showlegend = False
) 

trace4 = go.Bar(
    x = df7.iloc[:,0],
    y = df7.iloc[:,1],
    name = 'Note moyenne par professeur',
    showlegend = False
)  

#Global average value, shown as a threshold line
trace5 = go.Scatter(
    x = [" "],    
    y = [df1['Avg'].mean()],
    mode = 'text',
    text = ['Moyenne globale'],
    name = 'Moyenne globale',
    showlegend = False
) 

page_3_layout = html.Div([
    html.H1('Evaluation par Profil par étudiant ', style={'width': '1000px'}),
    html.Div(children='''
        Veuillez choisir un filtre
    '''),
    
        dcc.Tabs(id="tabs", value='tab_1', children=[
            dcc.Tab(label='Niveau de français', value='tab_1'),
            dcc.Tab(label='Formation', value='tab_2'),
            dcc.Tab(label='Site', value='tab_3'),
            dcc.Tab(label='Professeur', value='tab_4'),
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
                            'name' : 'Moyenne globale'
                        }],
                        'title' : 'Note moyenne par niveau de français',
                        'xaxis' : {
                            'title' : 'Niveau de français'
                        },
                        'yaxis' : {
                            'title' : 'Note moyenne'
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
                            'name' : 'Moyenne globale'
                        }],
                        'title' : 'Note moyenne par formation',
                        'xaxis' : {
                            'title' : 'Formation'
                        },
                        'yaxis' : {
                            'title' : 'Note moyenne'
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
                            'name' : 'Moyenne globale'
                        }],
                        'title' : 'Note moyenne par site',
                        'xaxis' : {
                            'title' : 'Site'
                        },
                        'yaxis' : {
                            'title' : 'Note moyenne'
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
                            'name' : 'Moyenne globale'
                        }],
                        'title' : 'Note moyenne par professeur',
                        'xaxis' : {
                            'title' : 'Professeur'
                        },
                        'yaxis' : {
                            'title' : 'Note moyenne'
                        },       
                    }
                }
            )
        ])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True,port='8055')
