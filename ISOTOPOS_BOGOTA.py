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
my_dataset = "https://raw.githubusercontent.com/hidabril/ISOTOPOS_BOGOTA/main/Resultados_mar.csv"
# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv(my_dataset)
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["Año_Mes"] = df["Fecha"].dt.strftime("%Y-%m")
print(df)
df.info()

#df = df.groupby(['Tipo', 'Fecha', 'Nombre', 'Nombre2', 'd2H', 'd18O', 'Tipo', 'd-excess', 'Mes'])
#df.reset_index(inplace=True)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

    #     html.Div(
    #     className="app-header",
    #     children=[
    #         html.Div('Universidad Nacional de Colombia', className="app-header--title")
    #     ]
    # ),



# App layout
app.layout = dbc.Container([
#Primer Div parte SUPERIOR
    html.Div([


#Espaciado para que no quede al raz las imagenes
        html.Div(
        className="app-header",
        children=[
            html.Div( html.Br(), className="app-header--title")
        ]
    ),
#Espaciado para que no quede al raz las imagenes
#Imagenes, logo unal y logho hyds"
        html.Div(
        html.Center([html.Img(src='/assets/HYDS.png', width="150" , height="75"),'\u00A0 \u00A0 \u00A0 \u00A0',html.Img(src='/assets/un.png', width="350" , height="150")]),

    style={
    'background': '#DCF3F6',
    'opacity':'0.7',
    } 
    ),
#Imagenes, logo unal y logho hyds"

#Espaciado para que no quede al raz las imagenes

        html.Div(
        className="app-header",
        children=[
            html.Div( html.Br(), className="app-header--title")
        ]
    ),
#Espaciado para que no quede al raz las imagenes

#Estilo primer Div parte SUPERIOR 

],
    style={
        # 'background-image': 'url("/assets/Hided.PNG")',
        # 'backgroundRepeat': 'no-repeat',
        # 'backgroundPosition': 'center'

        'background-image': 'url("https://www.eltiempo.com/uploads/2021/06/10/60c2b981ab0d9.jpeg")',
        'backgroundRepeat': 'no-repeat', 'backgroundPosition': 'center', 'backgroundSize': 'cover'

    }
),

#Primer Div parte SUPERIOR

#Titulo isotopos

        html.Hr(),

        html.H1(
        children='Isotopos Bogotá',
        style={
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Div(children='Implementar una red de monitoreo que permita mediante la implementación de herramientas isotópicas e hidrogeoquímicas establecer los patrones de flujo de agua subterránea y sus interacciones con fuentes superficiales en la Bogotá región, para así identificar:\
                        Riesgos en el abastecimiento asociados a la afectación de páramos ante efectos de cambio climático. \
                        Riesgos por subsidencias ante la sobreexplotación de los acuíferos de Bogotá región. \
                        Riesgos por inestabilidades asociadas a eventos de precipitación extrema más frecuentes o conexiones erradas del sistema de acueducto y alcantarillado. \
                        Afectación de los servicios ecosistémicos ante la afectación de las conexiones agua superficial-agua subterránea.', style={
        'textAlign': 'center',
        'color': '#FFFFFF'
    }),

#Titulo isotopos

#Graficas
    dbc.Row([
            html.Label('Seleccionar las estaciones de interes'),
            dcc.Dropdown(id="slct_estación",
                        options=[
                            {"label": "TOT Totalizador Hidráulica", "value": "TOT Hidráulica (Lluvia)"},
                            {"label": "PA-25 Genética", "value": "Genetica (30m)"},
                            {"label": "PZ-227", "value": "PZ-227-IV-D-103 (140m)"},
                            {"label": "POZO-227", "value": "Pozo 227-IV-D-103 (250m)"},
                            {"label": "Hidráulica 03", "value": "Hidraulica3 (7m)"}],
                        value = ["TOT Hidráulica (Lluvia)","Genetica (30m)","PZ-227-IV-D-103 (140m)","Pozo 227-IV-D-103 (250m)","Hidraulica3 (7m)"],
                        multi=True,
                        ),
            html.Label('Seleccionar los meses de interes'),
            dcc.Dropdown(id="slct_date",
                          options=[
                              {"label" : '2022-11', "value" : '2022-11'}, 
                              {"label" : '2022-12', "value" : '2022-12'}, 
                              {"label" : '2023-01', "value" : '2023-01'}, 
                              {"label" : '2023-02', "value" : '2023-02'}, 
                          ],
                          value=['2022-11','2022-12','2023-01','2023-02'],
                          multi=True,
                        )
                        
    ]),

    dbc.Row([
        
        dcc.Graph(id='puntos-muestreo', figure={}),

        dcc.Checklist(id='slct_Linea',
                      options=[
                            {"label" : "Linea Meteórica Colombia - δ²H = 8.02δ¹⁸H + 12.1 Saylor et al (2009)", "value" : "Colombia"},
                            {"label" : "Linea Meteórica Bogotá", "value" : "Bogotá"}],
                      value = ["Colombia"],
                      inline=True,
                    ),

        dcc.Graph(id='curva', figure={},),

        dcc.Graph(id='d2H', figure={}),

        dcc.Graph(id='d18O', figure={}),

        dcc.Graph(id='dexcess', figure={}),
    ]),
  
])


#Callback
@app.callback(
    [Output(component_id='curva', component_property='figure'),
     Output(component_id='puntos-muestreo', component_property='figure'),
     Output(component_id='d2H', component_property='figure'),
     Output(component_id='d18O', component_property='figure'),
     Output(component_id='dexcess', component_property='figure')],
    [Input(component_id='slct_estación', component_property='value'),
     Input(component_id='slct_date', component_property='value'),
     Input(component_id='slct_Linea', component_property='value')
     ]
)
def update_graph(option_slctd,option_slctd2,option_slctd3):
    print(option_slctd2)
    print(type(option_slctd2))

    dff = df.copy()
    dff = dff[dff["Linea"].isin(option_slctd3)]
    lineax = dff.d2hColombia
    lineay = dff.d18oColombia
    dff = dff[dff["Nombre2"].isin(option_slctd)]
    dff = dff[dff["Año_Mes"].isin(option_slctd2)]
    print(dff)

    d2h = dff.d2H
    d18o = dff.d18O
    Fecha = dff["Fecha"].dt.strftime("%Y-%m")
    dexcess = dff.dexcess

    container = px.scatter(
        data_frame=dff,
        x=d2h,
        y=d18o,
        color="Nombre2",
        symbol="Nombre2",
        labels=dict(d2H="δ²H ‰", d18O="δ¹⁸H ‰"),
    )
    
    container.add_trace(
        go.Scatter(
        x=lineax,
        y=lineay,
        mode='lines',
        )
    )
    containerd2H = px.line(
        data_frame=dff,
        x=Fecha,
        y=d2h,
        color="Nombre2",
        symbol="Nombre2",
        labels=dict(d2H="δ²H ‰"),
    )

    containerd18O = px.line(
        data_frame=dff,
        x=Fecha,
        y=d18o,
        color="Nombre2",
        symbol="Nombre2",
        labels=dict(d18O="δ¹⁸H ‰"),
    )

    containerdexcess = px.line(
        data_frame=dff,
        x=Fecha,
        y=dexcess,
        color="Nombre2",
        symbol="Nombre2",
        labels=dict(dexcess="d-excess ‰"),
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

    
    return container, fig, containerd2H, containerd18O, containerdexcess

if __name__ == '__main__':
    app.run_server()
