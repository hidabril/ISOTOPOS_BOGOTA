
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)


app = Dash(__name__)
server = app.server

mapbox_access_token = "pk.eyJ1IjoiYWJyaWxoaWQiLCJhIjoiY2xoY3J5dnlpMHU0ajNtbXR1MW80cHd0aiJ9.4D2V1tHsx7FS8HFveyaz1Q"
mapbox_style = "mapbox://styles/mapbox/streets-v12"

# In[16]:

my_dataset= "https://raw.githubusercontent.com/hidabril/ISOTOPOS_BOGOTA/main/Resultados_feb.csv"
# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv(my_dataset)
print(df)

#df = df.groupby(['Tipo', 'Fecha', 'Nombre', 'Nombre2', 'd2H', 'd18O', 'Tipo', 'd-excess', 'Mes'])
#df.reset_index(inplace=True)

Meses = [11,12,1]

DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8


# In[17]:


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Isotopos Bogotá HYDS", style={'text-align': 'center'}),
    
    dcc.Dropdown(id="slct_estación",
                 options=[
                     {"label": "TOT Totalizador Hidráulica", "value": "TOT Hidráulica (Lluvia)"},
                     {"label": "PA-25 Genética", "value": "Genetica (30m)"},
                     {"label": "PZ-227", "value": "PZ-227-IV-D-103 (140m)"},
                     {"label": "POZO-227", "value": "Pozo 227-IV-D-103 (250m)"},
                     {"label": "Hidráulica 03", "value": "Hidraulica3 (7m)"}],
                 multi=False,
                 value="TOT Hidráulica (Lluvia)",
                 style={'width': "40%"}
                 ),

    dcc.Graph(id='curva', figure={}),
    html.Br(),

    dcc.Graph(id='puntos-muestreo', figure={})
    
    
])

@app.callback(
    [Output(component_id='curva', component_property='figure'),
     Output(component_id='puntos-muestreo', component_property='figure')],
    [Input(component_id='slct_estación', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df.copy()
    dff = dff[dff["Nombre2"] == option_slctd]

    d2h = dff.d2H
    d18o = dff.d18O

    container = px.scatter(
        data_frame=dff,
        x=d2h,
        y=d18o,
    )
    
    #"La estación seleccionada es {}".format(option_slctd)

    site_lat = dff.Lat
    site_lon = dff.Lon
    site_text = dff.Nombre2

    # Plotly Express
    fig = go.Figure(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
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
                lat=4.6388,
                lon=-74.0814
            ),
            pitch=0,
            zoom=15,
            style=mapbox_style
        ),
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig

if __name__ == '__main__':
    app.run_server()


# In[ ]:
