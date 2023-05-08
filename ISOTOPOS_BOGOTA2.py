import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Mapbox configuration
mapbox_access_token = "pk.eyJ1IjoiYWJyaWxoaWQiLCJhIjoiY2xoY3J5dnlpMHU0ajNtbXR1MW80cHd0aiJ9.4D2V1tHsx7FS8HFveyaz1Q"
mapbox_style = "mapbox://styles/mapbox/streets-v12"


#Data
my_dataset= "https://raw.githubusercontent.com/hidabril/ISOTOPOS_BOGOTA/main/Resultados_feb.csv"
# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv(my_dataset)
print(df)

#df = df.groupby(['Tipo', 'Fecha', 'Nombre', 'Nombre2', 'd2H', 'd18O', 'Tipo', 'd-excess', 'Mes'])
#df.reset_index(inplace=True)



# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.H1("Isotopos Bogotá HYDS", style={'text-align': 'center'}),
            html.Label('Seleccionar las estaciones de interes'),
            dcc.Checklist(id="slct_estación",
                        options=[
                            {"label": "TOT Totalizador Hidráulica", "value": "TOT Hidráulica (Lluvia)"},
                            {"label": "PA-25 Genética", "value": "Genetica (30m)"},
                            {"label": "PZ-227", "value": "PZ-227-IV-D-103 (140m)"},
                            {"label": "POZO-227", "value": "Pozo 227-IV-D-103 (250m)"},
                            {"label": "Hidráulica 03", "value": "Hidraulica3 (7m)"}],
                        value = ["TOT Hidráulica (Lluvia)","Genetica (30m)","PZ-227-IV-D-103 (140m)","Pozo 227-IV-D-103 (250m)","Hidraulica3 (7m)"],
                        inline=True,
                        ),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='puntos-muestreo', figure={})
        ],width=6),

        dbc.Col([
            dcc.Graph(id='curva', figure={}),
        ],width=6)
    ]),
  
])


#Callback
@app.callback(
    [Output(component_id='curva', component_property='figure'),
     Output(component_id='puntos-muestreo', component_property='figure')],
    [Input(component_id='slct_estación', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df.copy()
    dff = dff[dff["Nombre2"].isin(option_slctd)]

    d2h = dff.d2H
    d18o = dff.d18O

    container = px.scatter(
        data_frame=dff,
        x=d2h,
        y=d18o,
        color="Nombre2",
        symbol="Nombre2"
    )
    
    site_lat = dff.Lat
    site_lon = dff.Lon
    site_text = dff.Nombre2

    fig = go.Figure(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
        ),
        text=site_text,
    ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=4.641,
                lon=-74.0814
            ),
            pitch=0,
            zoom=15,
            style=mapbox_style
        ),
    )

    return container, fig

if __name__ == '__main__':
    app.run_server()
