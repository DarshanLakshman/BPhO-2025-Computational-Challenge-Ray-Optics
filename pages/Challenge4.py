import dash
from dash import html, dcc, Output, Input
import numpy as np
import plotly.graph_objects as go

def challenge_4_code(c1=3e8, c2=3e8, y=10, L=10, Y=11):
    c = 3e8
    n1 = c / c1
    n2 = c / c2

    x = np.linspace(0, L, 1000)
    t = np.sqrt(x**2 + y**2) / (c / n1) + np.sqrt((L - x)**2 + Y**2) / (c / n2)

    idx_min = np.argmin(t)
    x_min = x[idx_min]
    t_min = t[idx_min]

    a_inc = np.arctan2(x_min, y)
    a_ref = np.arctan2(L - x_min, Y)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=t,
        mode='lines',
        name='Travel time'
    ))

    fig.add_trace(go.Scatter(
        x=[x_min], y=[t_min],
        mode='markers',
        marker=dict(color='red', size=10, symbol='x'),
        name='Minimum travel time'
    ))


    fig.add_annotation(
        x=1.02, y=0.95,
        xref="paper", yref="paper",
        text=f"sin(theta1)/c1: {np.sin(a_inc) / c1:.3e}",
        showarrow=False,
        font=dict(color="white"),
        align="left"
    )

    fig.add_annotation(
        x=1.02, y=0.91,
        xref="paper", yref="paper",
        text=f"sin(theta2)/c2: {np.sin(a_ref) / c2:.3e}",
        showarrow=False,
        font=dict(color="white"),
        align="left"
    )

    fig.add_annotation(
        x=1.02, y=0.87,
        xref="paper", yref="paper",
        text="Both equal (Snell's law)",
        showarrow=False,
        font=dict(color="white"),
        align="left"
    )

    fig.update_layout(
        title="Travel Time vs x",
        xaxis_title="x (m)",
        yaxis_title="Time (s)",
        template="plotly_dark",
        margin=dict(r=180)  
    )

    return fig



dash.register_page(__name__, path='/challenge4', name="Challenge 4", order=4)

layout = html.Div([
    html.Div([html.H1("Challenge 4"), html.Br(), html.Br()]),

    html.Div([
        html.Label("c1 (m/s):"), dcc.Input(id='c_1', type='number', value=3e8, step=1e6), html.Br(),html.Br(),
        html.Label("c2 (m/s):"), dcc.Input(id='c_2', type='number', value=3e8, step=1e6), html.Br(),html.Br(),
        html.Label("y    (m):"), dcc.Input(id='y', type='number', value=10, step=0.5), html.Br(),html.Br(),
        html.Label("L    (m):"), dcc.Input(id='L', type='number', value=10, step=0.5), html.Br(),html.Br(),
        html.Label("Y    (m):"), dcc.Input(id='Y', type='number', value=11, step=0.5), html.Br(),html.Br(),
        dcc.Graph(id="snell-graph")
    ])
])

@dash.callback(
    Output('snell-graph', 'figure'),
    Input('c_1', 'value'),
    Input('c_2', 'value'),
    Input('y', 'value'),
    Input('L', 'value'),
    Input('Y', 'value')
)
def update_figure(c1, c2, y, L, Y):
    return challenge_4_code(c1, c2, y, L, Y)
