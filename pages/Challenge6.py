import dash
from dash import html, dcc, Output, Input
import numpy as np
from PIL import Image
import plotly.graph_objects as go

def challenge_6_code(offset_x, offset_y, f_val=20, step=1):

    img = Image.open("test.jpg").convert("RGB").resize((40, 40))
    data = np.array(img)
    h, w, _ = data.shape

    yy, xx = np.mgrid[0:h, 0:w]
    xs = xx.flatten().astype(float)
    ys = yy.flatten().astype(float)

    x_pix = xs - w / 2 + offset_x * step
    y_pix = (h - ys) - h / 2 + offset_y * step

    colors = data.reshape(-1, 3)
    color_strings = np.array([f'rgb({r},{g},{b})' for r, g, b in colors])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, 0],
        y=[-100, 100],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Lens axis (x=0)'
    ))

    object_mask = x_pix > 0
    fig.add_trace(go.Scattergl(
        x=x_pix[object_mask],
        y=y_pix[object_mask],
        mode='markers',
        marker=dict(color=color_strings[object_mask], symbol = "square",size=4, opacity=0.7),
        name='Object'
    ))

    mask = x_pix > f_val
    X_img = x_pix.copy()
    Y_img = y_pix.copy()

    X_img[mask] = -f_val / (x_pix[mask] - f_val) * x_pix[mask]
    Y_img[mask] = (y_pix[mask] / x_pix[mask]) * X_img[mask]

    image_mask = X_img < 0
    fig.add_trace(go.Scattergl(
        x=X_img[image_mask],
        y=Y_img[image_mask],
        mode='markers',
        marker=dict(color=color_strings[image_mask], symbol = "square",size=4, opacity=0.7),
        name='Image'
    ))


    fig.update_layout(
        title=f"Real, inverted image of an object, Thin lens: f={f_val}",
        xaxis=dict(scaleanchor="y"),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig

dash.register_page(__name__, path='/challenge6', name="Challenge 6", order=6)

# Layout
layout = html.Div([
    html.Div([
        html.Button('up', id='up-nclicks', n_clicks=0),
        html.Button('down', id='down-nclicks', n_clicks=0),
        html.Button('left', id='left-nclicks', n_clicks=0),
        html.Button('right', id='right-nclicks', n_clicks=0),
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Label("Focal Length (f) in px:  "),
        dcc.Input(id="f_val", type="number", placeholder="focal length (pixels)", value=20)
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.H1("Challenge 6"),
        dcc.Graph(id="c6")
    ])
])

# Callback
@dash.callback(
    Output('c6', 'figure'),
    Input('up-nclicks', 'n_clicks'),
    Input('down-nclicks', 'n_clicks'),
    Input('left-nclicks', 'n_clicks'),
    Input('right-nclicks', 'n_clicks'),
    Input('f_val', 'value')
)
def update_figure(up_clicks, down_clicks, left_clicks, right_clicks, f_val):
    offset_y = 20 + (up_clicks or 0) - (down_clicks or 0)
    offset_x = 50 + (right_clicks or 0) - (left_clicks or 0)
    return challenge_6_code(offset_x, offset_y, f_val=f_val or 2)