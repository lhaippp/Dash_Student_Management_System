import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
import plotly.plotly as py
from dashboard_prof import dashboard_prof 


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
          <a class="nav-link" href="">
            <i class="fas fa-fw fa-tachometer-alt"></i>
            <span>Dashboard</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="charts.html">
            <i class="fas fa-fw fa-chart-area"></i>
            <span>Evolution</span></a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="tables.html">
            <i class="fas fa-fw fa-table"></i>
            <span>Tableaux</span></a>
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
app.layout = html.Div(className='col-12 mb-6',children=[
    html.H1(children='Aperçu général des performances'),

    html.Div(children='''
        Veuillez choisir un Groupe
    '''),
   dcc.Dropdown(
        options=[{'label': 'Groupe ' + str(i), 'value': i} for i in df_students.id_groupe.unique()],
        id='dropdown',
        value='1'
    ),
           html.Div(children='''
        Veuillez choisir une catégorie
    '''),
    dcc.Dropdown(
        options=[{'label': str(i), 'value': i} for i in df_fait.categorie.unique()],
        id='dropdown_categorie',
        placeholder="Toutes les catégories",
    ),
           
           
    html.H3(id='output'),
    
    html.Div(id='graph_div'),
    
    dcc.Graph(
     figure=go.Figure(
      data = [go.Scatterpolar(
      r = [39, 28, 8, 7, 28, 39],
      theta = [i for i in df_fait.categorie.unique().tolist()],
      fill = 'toself'
      )],
    
      layout = go.Layout(
      polar = dict(
      radialaxis = dict(
      visible = True,
      range = [0, 50])),
      showlegend = False
      )
     )
    ),
      
    html.Div(id='table_div'),
    
    html.Div(id='heatmap_div')
          
])

@app.callback(Output('output', 'children'), [Input('dropdown', 'value')])
def display_output(value):
    return 'Visulisation des résultats pour Groupe '+str(value)

@app.callback(Output('table_div', 'children'), [Input('dropdown', 'value')])
def update_table(value):
    return  dash_table.DataTable(
            id='table',
            #columns=[{"name": i, "id": i} for i in df_students.ix[(df_students["id_groupe"]==value),['nom_ele','prenom_ele']]],
            columns=[{"name": i, "id": i} for i in df_students.loc[(df_students["id_groupe"]==value),]],
            data=df_students.loc[(df_students["id_groupe"]==value),].to_dict("rows"),),
            
@app.callback(Output('graph_div', 'children'), [Input('dropdown', 'value')])
def update_graph(value):
    df_buffer = df_students.loc[(df_students["id_groupe"]==value),['nom','prenom']]
    buffer = df_buffer['nom']+' '+df_buffer['prenom']
    return dcc.Graph(
    figure=go.Figure(
        data=[
            go.Bar(
                x=buffer.tolist(),
                y=[40, 46, 32, 57, 44],
                name='Réponses correctes',
                marker=go.bar.Marker(
                    color='rgb(55, 83, 109)'
                )
            ),
            go.Bar(
                x=buffer.tolist(),
                y=[20, 14, 28, 3, 16],
                name='Réponses incorrectes',
                marker=go.bar.Marker(
                    color='rgb(26, 118, 255)'
                )
            ),
            go.Bar(
                x=buffer.tolist(),
                y=[5, 11, 2, 3,12],
                name='Pas de réponses',
                marker=go.bar.Marker(
                    color='rgb(0, 0, 0)'
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
      
        
@app.callback(Output('heatmap_div', 'children'), [Input('dropdown', 'value')])
def update_heatmap(id_groupe=1):
    
    df = dashboard_prof.df_heatmap(id_groupe)
    yticks = df['nom'].str.cat(df['prenom'],sep=' ').values.tolist()
    xticks = [x for x in df.columns if x not in ['id_groupe','id_eleve','nom','prenom']]
    
    layout = go.Layout(
        autosize=False,
        width=100*len(xticks),
        height=100*len(yticks),
        margin=go.layout.Margin(
            l=150,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        xaxis=dict(
            showticklabels=True,
            tickangle=15,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=20,
                color='black'
            )
        ),
        yaxis=dict(
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=20,
                color='black'
            )
        ),
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff'
    )
    
    yticks = df['nom'].str.cat(df['prenom'],sep=' ').values.tolist()
    xticks = [x for x in df.columns if x not in ['id_groupe','id_eleve','nom','prenom']]
    trace = go.Heatmap(z=df[[x for x in df.columns if x not in ['id_groupe','id_eleve','nom','prenom']]].values,
                       y=yticks, ytype='array',
                       x= xticks, xtype='array',
                       colorscale = [[0,'#a80101'],[0.5,"#dbf287"],[1,"#619101"]],
    #                    connectgaps= False
                       xgap=1,
                       ygap=5
                      )
    data=[trace]
    fig = go.Figure(data=data, layout=layout)
    return dcc.Graph(figure = fig )


if __name__ == '__main__':
    app.run_server(debug=True,port='8055')
