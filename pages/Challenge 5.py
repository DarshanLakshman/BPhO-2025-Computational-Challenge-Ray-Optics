import dash
from dash import html, dcc, Output, Input
import numpy as np
from PIL import Image
import plotly.graph_objects as go

def challenge_5_code(offset_x, offset_y, step=10):
    img = Image.open("cat.jpeg").convert("RGB").resize((50, 50))
    data = np.array(img)
    h, w, d = data.shape

    # Bottom-left corner of original image at x = 10
    initial_x_offset = 10

    yy, xx = np.mgrid[0:h, 0:w]
    xs = xx.flatten()
    ys = yy.flatten()

    # Flip y axis so bottom-left is (0,0)
    ys = h - ys

    colors = data.reshape(-1, 3)
    color_strings = [f'rgb({r},{g},{b})' for r, g, b in colors]

    xs_trans = xs + initial_x_offset + offset_x * step
    ys_trans = ys + offset_y * step

    # Reflection about x=0: reflected_x = -original_x
    xs_reflected = -xs_trans
    ys_reflected = ys_trans

    fig = go.Figure()

    # Mirror line at x=0
    fig.add_trace(go.Scatter(
        x=[0, 0],
        y=[-100, 100],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Mirror Line'
    ))

    # Original image
    fig.add_trace(go.Scattergl(
        x=xs_trans,
        y=ys_trans,
        mode='markers',
        marker=dict(color=color_strings, size=4, opacity=1),
        name='Original Image'
    ))

    # Reflected image
    fig.add_trace(go.Scattergl(
        x=xs_reflected,
        y=ys_reflected,
        mode='markers',
        marker=dict(color=color_strings, size=4, opacity=1),
        name='Reflected Image'
    ))

    fig.update_layout(
        xaxis=dict(scaleanchor="y"),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

dash.register_page(__name__, path='/challange5', name="Challenge 5", order=5)

layout = html.Div([
    html.Div([
        html.Button('up', id='up-nclicks', n_clicks=0),
        html.Button('down', id='down-nclicks', n_clicks=0),
        html.Button('left', id='left-nclicks', n_clicks=0),
        html.Button('right', id='right-nclicks', n_clicks=0),
    ], style={'marginBottom': '20px'}),
    html.Div([
        html.H1("Challenge 5 - Plane Mirror Reflection"),
        dcc.Graph(id="mirror")
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
    offset_y = u - d
    offset_x = r - l
    return challenge_5_code(offset_x, offset_y)
