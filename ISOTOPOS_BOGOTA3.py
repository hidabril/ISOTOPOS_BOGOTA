import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Mapbox configuration
mapbox_access_token = "pk.eyJ1IjoiYWJyaWxoaWQiLCJhIjoiY2xoY3J5dnlpMHU0ajNtbXR1MW80cHd0aiJ9.4D2V1tHsx7FS8HFveyaz1Q"
mapbox_style = "mapbox://styles/mapbox/streets-v12"


#Data
my_dataset = "https://raw.githubusercontent.com/hidabril/ISOTOPOS_BOGOTA/main/Resultados_mar2.csv"

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
app.layout = html.Div([

html.Div([
#Primer Div parte SUPERIOR


#Espaciado para que no quede al raz las imagenes
        html.Div(
        className="app-header",
        children=[
            html.Div( html.Br(), className="app-header--title",
                     style={
                            'background': '#FFFFFF',
                            'opacity':'0.7',
                            }
                     )
        ]
    ),
#Espaciado para que no quede al raz las imagenes
#Imagenes, logo unal y logho hyds"
        html.Div(
        html.Center([html.Img(src='/assets/HYDS.png', width="150" , height="75"),'\u00A0 \u00A0 \u00A0 \u00A0',html.Img(src='/assets/un.png', width="350" , height="150")]),

    style={
    'background': '#FFFFFF',
    'opacity':'0.7',
    } 
    ),
#Imagenes, logo unal y logho hyds"

#Espaciado para que no quede al raz las imagenes

        html.Div(
        className="app-header",
        children=[
            html.Div( html.Br(), className="app-header--title",
                     style={
                            'background': '#FFFFFF',
                            'opacity':'0.7',
                            }
                     )
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

    html.Div(
    className="toast show",
    children=[
        html.Div(html.P(html.H1('\u00A0 Isotopos Bogotá')),className="app-header--title",style={'textAlign':'left'})
    ]
    ),



    html.Div(children=[
        html.Div(html.P(['Implementar una red de monitoreo que permita mediante la implementación de herramientas isotópicas e hidrogeoquímicas establecer los patrones de flujo de agua subterránea y sus interacciones con fuentes superficiales en la Bogotá región, para así identificar:',html.Ul([html.Li('Riesgos en el abastecimiento asociados a la afectación de páramos ante efectos de cambio climático.'),html.Li("Riesgos por subsidencias ante la sobreexplotación de los acuíferos de Bogotá región."),html.Li("Riesgos por inestabilidades asociadas a eventos de precipitación extrema más frecuentes o conexiones erradas del sistema de acueducto y alcantarillado."), html.Li("Afectación de los servicios ecosistémicos ante la afectación de las conexiones agua superficial-agua subterránea.")])],
                 className="alert alert-dismissible alert-light",
                 style={
                     'textAlign':'left'
                     })
    )]
    ),

#Titulo isotopos

#Graficas
    
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
                        {"label" : '2023-03', "value" : '2023-03'}, 
                    ],
                    value=['2022-11','2022-12','2023-01','2023-02','2023-03'],
                    multi=True,
                ),
                        
    #html.Div(
        #style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100vh'},
        #children=[
        
    dcc.Graph(id='puntos-muestreo', figure={}),

    # dcc.Checklist(id='slct_Linea',
    #               options=[
    #                     {"label" : "Linea Meteórica Colombia - δ²H = 8.02δ¹⁸O + 12.1 Saylor et al (2009) ", "value" : "Colombia"},
    #                     {"label" : "Linea Meteórica Bogotá - δ²H = 8.18δ¹⁸O + 11.63 GNIP RMA", "value" : "Bogotá"}],
    #               value = ["Colombia"],
    #               inline=True,
    #             ),

    dcc.Graph(id='curva', figure={},),

    dcc.Graph(id='d2H', figure={}),

    dcc.Graph(id='d18O', figure={}),

    dcc.Graph(id='dexcess', figure={}),

    #]),

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
     #Input(component_id='slct_Linea', component_property='value')
     ]
)
def update_graph(option_slctd,option_slctd2,):
    print(option_slctd2)
    print(type(option_slctd2))

    
    dff = df.copy()

    lineax = dff['d18oMeteo']
    lineaycol = dff['d2hCol']
    lineayBog = dff['d2hBog']
    #dff = dff[dff["Linea"].isin(option_slctd3)]
  
    # if option_slctd3 == 'Colombia':
    #     lineay = dff['d2hCol']
    # elif option_slctd3 == 'Bogotá':
    #     lineay = dff['d2hBog']
    # lineax = dff.d18oMeteo

    dff = dff[dff["Nombre2"].isin(option_slctd)]
    dff = dff[dff["Año_Mes"].isin(option_slctd2)]
    print(dff)

    d2h = dff.d2H
    d18o = dff.d18O
    Fecha = dff["Año_Mes"]
    dexcess = dff.dexcess

    container = px.scatter(
        data_frame=dff,
        x=d18o,
        y=d2h,
        color="Nombre2",
        symbol="Año_Mes",
        template="simple_white",
        labels=dict(d2H="δ²H ‰", d18O="δ¹⁸O ‰", Nombre2="Punto de muestreo"),
        title="Linea Meteórica",
    )
    
    container.add_trace(
        go.Scatter(
        x=lineax,
        y=lineaycol,
        name="Linea Meteórica Colombia",
        )
    )
    container.add_trace(
        go.Scatter(
        x=lineax,
        y=lineayBog,
        name="Linea Meteórica Bogotá",
        )

    )
    containerd2H = px.line(
        data_frame=dff,
        x=Fecha,
        y=d2h,
        color="Nombre2",
        symbol="Nombre2",
        template="simple_white",
        labels=dict(d2H="δ²H ‰" , Año_Mes="Fecha de muestra" , Nombre2="Punto de muestreo"),
        title="Variación de Deuterio en el tiempo",
    )

    containerd18O = px.line(
        data_frame=dff,
        x=Fecha,
        y=d18o,
        color="Nombre2",
        symbol="Nombre2",
        template="simple_white",
        labels=dict(d18O="δ¹⁸H ‰" , Año_Mes="Fecha de muestra" , Nombre2="Punto de muestreo"),
        title="Variación de Oxigeno 18 en el tiempo",
    )
    
    containerdexcess = px.line(
        data_frame=dff,
        x=Fecha,
        y=dexcess,
        color="Nombre2",
        symbol="Nombre2",
        template="simple_white",
        labels=dict(dexcess="d-excess ‰" , Año_Mes="Fecha de muestra" , Nombre2="Punto de muestreo" ),
        title="Variación de d-excess en el tiempo",
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
        title = 'Puntos de muestreos',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=4.641,
                lon=-74.0814
            ),
            pitch=0,
            zoom=15,
            style=mapbox_style,
        ),
    )

    
    return container, fig, containerd2H, containerd18O, containerdexcess

if __name__ == '__main__':
    app.run()
