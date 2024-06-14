from dash import dash, Dash, html, dcc, _dash_renderer, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_leaflet as dl
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
from datetime import date, datetime

_dash_renderer._set_react_version('18.2.0')

# Data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# App definition
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, "https://unpkg.com/@mantine/dates@7/styles.css"])

# Gridded layout
app.layout = dmc.MantineProvider(children=[
    
    # Grid container
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
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.Select(
                            radius=0,
                            size="sm", 
                            id="dropdown-selection",
                            value="Italy",
                            data=df.country.unique(),
                            w='full',
                            searchable=True,
                            placeholder="Choose Country",
                            leftSection=DashIconify(icon="radix-icons:magnifying-glass"),
                            rightSection=DashIconify(icon="radix-icons:chevron-down"),
                        ),
                        span=6,
                        pr=0
                    ),
                    dmc.GridCol(
                        dmc.DatePicker(
                            w='full', 
                            radius=0, 
                            type="range", 
                            numberOfColumns=2,
                            placeholder="Date range",
                            leftSection=DashIconify(icon="radix-icons:calendar")
                        ),
                        span=6
                    ),
                ]
            )
        ]),
        
        # KPI section
        html.Div(className="kpi-1", children=[html.H3("KPI-1")]),
        html.Div(className="kpi-2", children=[html.H3("KPI-2")]),
        
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
                className="ag-theme-material",
                columnSize="sizeToFit",
                dashGridOptions={"rowHeight": 40, "pagination": True},
                style={"height":"100%"},
                getRowStyle={
                    'styleConditions': [{
                        'condition': 'params.node.rowIndex % 2 == 0',
                        'style': {'backgroundColor': '#f5f5f5'}
                    }]
                }
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