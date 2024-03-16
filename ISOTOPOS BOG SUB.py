import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Mapbox access token (replace with your own)
mapbox_access_token = "pk.eyJ1IjoiYWJyaWxoaWQiLCJhIjoiY2xoY3J5dnlpMHU0ajNtbXR1MW80cHd0aiJ9.4D2V1tHsx7FS8HFveyaz1Q"
mapbox_style = "mapbox://styles/mapbox/outdoors-v12"
# Dataset URL
my_dataset = "https://raw.githubusercontent.com/hidabril/ISOTOPOS_BOGOTA/main/Base_PGW_FULL.csv"

# Read data
df = pd.read_csv(my_dataset)
dff = df.copy()

# Site locations
site_lat = dff.Lat
site_lon = dff.Lon
site_PGW = dff["P/GW"]
site_tipo = dff.TIPO
cmax = df["P/GW"].sort_values(ascending=False).iloc[1]
cmin = df["P/GW"].sort_values(ascending=False).iloc[-1]
print(cmin)

# Create Dash app
app = dash.Dash(__name__)

# Function to create filtered scatter plot figure based on selected points
def get_figure(selected_points):
    if selected_points and selected_points["points"]:
        filtered_df = dff.iloc[
            [
                p["pointNumber"]
                for p in selected_points["points"]
                if "pointNumber" in p
            ]
        ]
    else:
        filtered_df = dff.copy()
        
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_df["OXIG_18"],
            y=filtered_df["DEUT_2H"],
            mode="markers"
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=[-9.394303],
            y=[-65.224002],
            mode="markers"
        )
    )
    
    fig.update_layout(
        template="plotly_white",
        title="Linea Meteórica"
    )
    
    fig.show()
    return fig

# App layout
app.layout = dbc.Container([
    html.Div([
        html.H1(children="Isotopes Bogotá", style={"textAlign": "left"}),
        html.Hr(),
        html.Div([
            dcc.Graph(
                id="sampling-points-map",
                style={"height": "700px",'display': 'inline-block'},
                figure=go.Figure(
                    go.Scattermapbox(
                        lat=site_lat,
                        lon=site_lon,
                        mode="markers",
                        marker = dict(
                               size = 8,
                               symbol = 'circle',
                               colorscale = 'viridis',
                               color = site_PGW,
                               colorbar_title="P/GW",
                               colorbar_orientation="h",
                               cmax=cmax,
                               cmin=cmin,

                           ),
                    )
                ).update_layout(
                    autosize=True,
                    hovermode="closest",
                    title="Puntos de muestreos",
                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(lat=4.91, lon=-73.96),
                        pitch=0,
                        zoom=8.5,
                        style=mapbox_style,
                    ),
                ),
                
            ),
            dcc.Graph(
                id="isotopic-composition",
                style={"height": "700px",'display': 'inline-block'},
                figure=get_figure(None),  # Initial figure with all data
            ),
        ], style={"display": "inline-block"}),
    ]),
])

# Callback to update scatter plot based on selected points in the map
@app.callback(
    Output("isotopic-composition", "figure"),
    Input("sampling-points-map", "selectedData"),
)
def update_isotopic_composition(selected_points):
    return get_figure(selected_points)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)