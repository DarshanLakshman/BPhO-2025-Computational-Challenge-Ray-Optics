import dash
from dash import html, dcc

import numpy as np
import plotly.graph_objects as go
from helpers import get_colour

def challenge_1a_graph():
    wavelengths = np.linspace(400, 800, 1000)

    x = wavelengths / 1000.0
    a = np.array([1.03961212, 0.231792344, 1.01146945])
    b = np.array([0.00600069867, 0.0200179144, 103.560653])

    y = np.zeros_like(x)
    for k in range(len(a)):
        y += (a[k] * x**2) / (x**2 - b[k])

    n_values = np.sqrt(1 + y)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wavelengths, y=n_values, mode='lines', name='n(λ)'))
    fig.update_layout(
        title="Refractive Index vs Wavelength",
        xaxis_title="Wavelength (nm)",
        yaxis_title="Refractive Index",
        template='plotly_white'
    )

    return fig

def challenge_1b_graph():
    frequency = np.linspace(405 * 10 ** 12, 790 * 10 ** 12, 1000).tolist()
    refractive_index = [((1 / (1.731 - 0.261 * (f / (10 ** 15)) ** 2)) ** 0.5 + 1) ** 0.5 for f in frequency]
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
    [
        html.Div([
                html.H1("Challenge 1 - Model of Refractive Index of Crown Glass") 
        ]),

        html.Div([
            dcc.Graph(id="c1-a", figure = challenge_1a_graph())
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id="c1-b", figure = challenge_1b_graph())
        ], style={'width': '48%', 'display': 'inline-block', 'float':'right'})
    ]
)
