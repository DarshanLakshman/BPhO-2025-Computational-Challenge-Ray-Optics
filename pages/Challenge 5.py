import dash
from dash import html, dcc, Output, Input
import numpy as np
from PIL import Image
import plotly.graph_objects as go

img = Image.open("cat.jepg").convert("RGB").resize((50, 50))
data = np.array(img)
h, w, _ = data.shape
yy, xx = np.mgrid[0:h, 0:w]
xs = xx.flatten()
ys = h - yy.flatten() 
colors = data.reshape(-1, 3)
color_strings = [f'rgb({r},{g},{b})' for r, g, b in colors]

step = 10
margin_from_axis = 10  

def create_figure(offset_x, offset_y):
    shift_x = offset_x * step + margin_from_axis
    shift_y = offset_y * step

    fig = go.Figure()

    fig.add_trace(go.Scattergl(
        x=[0, 0],
        y=[-200, 200],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Mirror Line'
    ))

    fig.add_trace(go.Scattergl(
        x=xs + shift_x,
        y=ys + shift_y,
        mode='markers',
        marker=dict(color=color_strings, size=5, opacity=1),
        name='Original'
    ))

    fig.add_trace(go.Scattergl(
        x=-(xs + shift_x),
        y=ys + shift_y,
        mode='markers',
        marker=dict(color=color_strings, size=2, opacity=1),
        name='Reflected'
    ))

    fig.update_layout(
        xaxis=dict(scaleanchor="y", visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )

    return fig

dash.register_page(__name__, path='/challenge5', name="Challenge 5", order=5)

layout = html.Div([
    html.Div([
        html.Button('up', id='up-nclicks', n_clicks=0),
        html.Button('down', id='down-nclicks', n_clicks=0),
        html.Button('left', id='left-nclicks', n_clicks=0),
        html.Button('right', id='right-nclicks', n_clicks=0),
    ]),
    html.Div([
        html.H1("Challenge 5 - Plane Mirror Reflection"),
        html.Br(),
        dcc.Graph(id="mirror", config={"displayModeBar": False})
    ])
])

@dash.callback(
    Output('mirror', 'figure'),
    Input('up-nclicks', 'n_clicks'),
    Input('down-nclicks', 'n_clicks'),
    Input('left-nclicks', 'n_clicks'),
    Input('right-nclicks', 'n_clicks')
)
def update_figure(u, d, l, r):
    return create_figure(r - l, u - d)
