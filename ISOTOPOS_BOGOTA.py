#!/usr/bin/env python
# coding: utf-8

# In[15]:


from jupyter_dash import JupyterDash
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)


app = JupyterDash(__name__)


# In[16]:


# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv("Resultados_feb.csv")

#df = df.groupby(['Tipo', 'Fecha', 'Nombre', 'Nombre2', 'd2H', 'd18O', 'Tipo', 'd-excess', 'Mes'])
#df.reset_index(inplace=True)

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

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "TOT Totalizador Hidráulica", "value": 1},
                     {"label": "PA-25 Genética", "value": 2016},
                     {"label": "PZ-227", "value": 2017},
                     {"label": "POZO-227", "value": 2018},
                     {"label": "Hidráulica 03", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
    
    
])

if __name__ == '__main__':
    app.run_server()


# In[ ]:




