import dash
from dash import html, dcc, Output, Input
import numpy as np
import plotly.graph_objects as go

def challenge_3_graph(y, n, L):
    c = 3*10**8

    xs = np.linspace(0, L, 1000).tolist()
    t = [((x ** 2 + y ** 2) ** 0.5 / (c / n)) + (((L - x) ** 2 + y ** 2) ** 0.5 / (c / n)) for x in xs]

    m = np.argmin(t)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=xs, y=t, mode='markers', name="Time"))

    fig.add_trace(go.Scatter(
        x=[xs[m]],
        y=[t[m]],
        mode='markers',
        marker=dict(color='red', size=10, symbol='x'),
        name='Minimum'
    ))

    fig.update_layout(
        xaxis=dict(range=[-L//2, L+1]), 
        yaxis=dict(range=[0.999*min(t), 1.001*max(t)]), 
        title="Fermat's Principle",
        xaxis_title="x",
        yaxis_title="Time (t)",
    )
    return fig


dash.register_page(__name__, path='/challenge3', name="Challenge 3", order=2)

layout = html.Div([
    html.H1("Challenge 3 - Fermat's Principle"),
    html.Br(),

    html.Div([
        html.Label("y (height from axis):"),
        dcc.Input(id='input-y', type='number', value=10, step=0.1),
    ], style={'margin': '10px'}),

    html.Div([
        html.Label("n (refractive index):"),
        dcc.Input(id='input-n', type='number', value=1, step=0.1),
    ], style={'margin': '10px'}),

    html.Div([
        html.Label("L (total horizontal distance):"),
        dcc.Input(id='input-L', type='number', value=2, step=0.1),
    ], style={'margin': '10px'}),

    dcc.Graph(id="fermat-graph")
])

@dash.callback(
    Output('fermat-graph', 'figure'),
    Input('input-y', 'value'), 
    Input('input-n', 'value'),
    Input('input-L', 'value'),
)
def update_figure(y, n, L):
    return challenge_3_graph(y, n, L)
