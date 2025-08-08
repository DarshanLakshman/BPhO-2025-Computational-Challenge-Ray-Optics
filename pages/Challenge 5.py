import dash
from dash import html, dcc, Output, Input
import numpy as np
from PIL import Image
import plotly.graph_objects as go

# Constants
step = 10
margin_from_axis = 10

# Load and preprocess image once
img = Image.open("cat.jpeg").convert("RGB").resize((50, 50))
data = np.array(img)  # (h, w, 3)
h, w, _ = data.shape

# Precompute coordinates and color strings once
yy, xx = np.mgrid[0:h, 0:w]
xs_base = xx.flatten()
ys_base = h - yy.flatten()  # invert y for display
colors = data.reshape(-1, 3)
color_strings = np.char.add('rgb(', np.char.add(colors[:, 0].astype(str), 
                    np.char.add(',', np.char.add(colors[:, 1].astype(str), 
                    np.char.add(',', np.char.add(colors[:, 2].astype(str), ')'))))))

# Figure generation function (fast)
def create_figure(offset_x, offset_y):
    shift_x = offset_x * step + margin_from_axis
    shift_y = offset_y * step

    xs_shifted = xs_base + shift_x
    ys_shifted = ys_base + shift_y

    fig = go.Figure()

    # Mirror line
    fig.add_trace(go.Scattergl(
        x=[0, 0], y=[-200, 200],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        hoverinfo='skip',
        showlegend=False
    ))

    # Original image points
    fig.add_trace(go.Scattergl(
        x=xs_shifted,
        y=ys_shifted,
        mode='markers',
        marker=dict(color=color_strings, size=5),
        hoverinfo='skip',
        showlegend=False
    ))

    # Reflected image points
    fig.add_trace(go.Scattergl(
        x=-xs_shifted,
        y=ys_shifted,
        mode='markers',
        marker=dict(color=color_strings, size=2),
        hoverinfo='skip',
        showlegend=False
    ))

    fig.update_layout(
        xaxis=dict(scaleanchor="y", visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        dragmode=False
    )

    return fig

# Dash Page Registration
dash.register_page(__name__, path='/challenge5', name="Challenge 5", order=5)

# Layout
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

# Callback
@dash.callback(
    Output('mirror', 'figure'),
    Input('up-nclicks', 'n_clicks'),
    Input('down-nclicks', 'n_clicks'),
    Input('left-nclicks', 'n_clicks'),
    Input('right-nclicks', 'n_clicks')
)
def update_figure(u, d, l, r):
    return create_figure(r - l, u - d)
