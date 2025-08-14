import dash
from dash import html, dcc

import numpy as np
import plotly.express as px

def challenge_2_graph():
    u = [5*n for n in range(4,12)]
    v = [65.5, 40, 31, 27, 25, 23.1, 21.5, 20.5]

    x_vals = [1 / val for val in u]
    y_vals = [1 / val for val in v]

    x_np = np.array(x_vals)
    y_np = np.array(y_vals)

    m, c = np.polyfit(x_np, y_np, 1)

    y_fit = m * x_np + c

    fig = px.scatter(x=x_vals, 
                     y=y_vals,
                     labels={"x": "1/u", "y": "1/v"})
    
    fig.add_scatter(x=x_vals, 
                    y=y_fit, 
                    mode='lines', 
                    name=f'Line of Best Fit <br> Gradient = {m:3f} <br> => Veracity = {1/m:3f}')
    

    return fig



dash.register_page(__name__, path='/challange2', name = "Challenge 2", order = 2)

layout = html.Div(
    children=[
        html.Div(
            children= [
                html.H1("Challenge 2 - Veracity of thin lens"), 
                html.Br(),
                dcc.Graph(id = "veracity graph", figure = challenge_2_graph())
            ]
        )
    ]
)
