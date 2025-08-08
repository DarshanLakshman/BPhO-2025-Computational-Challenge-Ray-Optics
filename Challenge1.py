import dash
from dash import html, dcc

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

def get_colour(f):
    f = f / (10 ** 12)
    if f < 405:
        return 0, 0, 0
    elif 405 <= f < 480:
        t = (f - 405) / 75
        return t, 0, 0
    elif 480 <= f < 510:
        t = (f - 480) / 30
        return 1, 0.5 * t, 0
    elif 510 <= f < 530:
        t = (f - 510) / 20
        return 1, 0.5 + 0.5 * t, 0
    elif 530 <= f < 600:
        t = (f - 530) / 70
        return 1 - t, 1, 0
    elif 600 <= f < 620:
        t = (f - 600) / 20
        return 0, 1, t
    elif 620 <= f < 680:
        t = (f - 620) / 60
        return 0, 1 - t, 1
    elif 680 <= f <= 790:
        t = (f - 680) / 110
        return 0.5 * t, 0, 1
    else:
        return 0, 0, 0

def challenge_1_graph():
    frequency = np.linspace(405 * 10 ** 12, 790 * 10 ** 12, 1000).tolist()
    refractive_index = [((1 / (1.731 - 0.261 * (f / (10 ** 15)) * 2)) * 0.5 + 1) * 0.5 for f in frequency]
    colours = [f"rgb{tuple(x*256 for x in get_colour(f))}" for f in frequency]

    fig = go.Figure()

    for i in range(len(frequency)):
        fig.add_trace(go.Scatter(
            x=[frequency[i]], y=[refractive_index[i]],
            mode='markers',
            marker=dict(color=colours[i], size=15)
        ))
    
    fig.update_layout(showlegend=False)


    return fig



dash.register_page(__name__, path='/challange1', name = "Challenge 1", order = 1)

layout = html.Div(
    children=[
        html.Div(
            children= [
                html.H1("Challenge 1 - Model of Refractive Index of Crown Glass") ,
                html.Br(),
                dcc.Graph(id = "refractive index graph", figure = challenge_1_graph())

            ]
        )
    ]
)