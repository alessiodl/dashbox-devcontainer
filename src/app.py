from dash import dash, Dash, html, dcc, _dash_renderer, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_leaflet as dl
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd

_dash_renderer._set_react_version('18.2.0')

# Data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# App definition
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Gridded layout
app.layout = dmc.MantineProvider(children=[
    html.Div(id='main-container', children=[
        # Header section
        html.Div(className="header", children=[
            html.H4(className="header-title", children=f'Boilerplate app on Dash v. {dash.__version__}'),
        ]),
        
        # Map section
        html.Div(className="map-container", children=[
            dl.Map(dl.TileLayer(), center=[43,12], zoom=4, style={'height': '100%'})
        ]),
        
        # Filters section
        html.Div(className="filters-container", children=[
            # dcc.Dropdown(df.country.unique(), 'Italy', id='dropdown-selection')
            dmc.Select(
                radius=0,
                size="sm", 
                id="dropdown-selection",
                value="Italy",
                data=df.country.unique(),
                # w=200,
                # mb=10,
            )
        ]),
        
        # KPI section
        html.Div(className="kpi-1", children=["KPI 1"]),
        html.Div(className="kpi-2", children=[]),
        
        # Chart section
        html.Div(className="chart-container", children=[
            dcc.Graph(id='graph-content', style={"height":"100%"})
        ]),
        
        # Table section
        html.Div(className="table-container", children=[
            dag.AgGrid(
                id="myGrid",
                columnDefs= [{"field": x, } for x in df.columns],
                rowData= df.to_dict('records'),
                className="ag-theme-alpine",
                columnSize="sizeToFit",
                dashGridOptions={"rowHeight": 30, "pagination": True},
                style={"height":"100%"}
            ),
        ])
    ])
])

# Callbacks

@callback(
    Output('graph-content', 'figure'),
    Output('myGrid','rowData'),
    Input('dropdown-selection', 'value')
)
def update_vizs(value):
    dff = df[df.country==value]
    
    fig = px.bar(dff, x='year', y='pop', color_discrete_sequence=['#023e8a'])
    fig.update_layout(plot_bgcolor='white')
    
    rows = dff.to_dict('records')
    
    return fig, rows 


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)