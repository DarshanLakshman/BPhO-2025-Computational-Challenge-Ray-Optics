import dash
from dash import html, dcc, Output, Input
import numpy as np
from PIL import Image
import plotly.graph_objects as go

def challenge_9_code(offset_x, offset_y, R=75, step=1):

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

    X_img = np.full_like(x_pix, np.nan)
    Y_img = np.full_like(y_pix, np.nan)


    alpha = 0.5 * np.arctan(y_pix / x_pix)
    k = x_pix/np.cos(2*alpha)
    Y_img = k * np.sin(alpha) / (k/R - np.cos(alpha) + (x_pix/y_pix) * np.sin(alpha))
    X_img = x_pix * Y_img/(y_pix)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, 0],
        y=[-100, 100],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Mirror axis'
    ))

    fig.add_trace(go.Scattergl(
        x=x_pix,
        y=y_pix,
        mode='markers',
        marker=dict(color=color_strings, symbol="square", size=4, opacity=0.7),
        name='Object'
    ))

    fig.add_trace(go.Scattergl(
        x=X_img,
        y=Y_img,
        mode='markers',
        marker=dict(color=color_strings, symbol="square", size=4, opacity=0.7),
        name='Reflected Image'
    ))

    mirror_y = np.linspace(-R, R, 200)
    mirror_x = np.sqrt(R**2 - mirror_y**2)

    fig.add_trace(go.Scatter(
        x=mirror_x,
        y=mirror_y,
        mode='lines',
        line=dict(color='blue', width=3),
        name='Concave Mirror'
    ))

    fig.update_layout(
        title=f"Reflection in vertical concave mirror with radius R={R}",
        xaxis=dict(scaleanchor="y"),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig


dash.register_page(__name__, path='/challenge9', name="Challenge 9", order=9)

layout = html.Div([
    html.Div([
        html.Button('up', id='up-nclicks', n_clicks=0),
        html.Button('down', id='down-nclicks', n_clicks=0),
        html.Button('left', id='left-nclicks', n_clicks=0),
        html.Button('right', id='right-nclicks', n_clicks=0),
    ], style={'marginBottom': '20px'}),

     html.Div([
        html.Label("Radius:  "),
        dcc.Input(id="R", type="number", placeholder="Radius", value=75),
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.H1("Challenge 9 "),
        dcc.Graph(id="c9")
    ])
])


@dash.callback(
    Output('c9', 'figure'),
    Input('up-nclicks', 'n_clicks'),
    Input('down-nclicks', 'n_clicks'),
    Input('left-nclicks', 'n_clicks'),
    Input('right-nclicks', 'n_clicks'),
    Input('R', 'value')
)
def update_figure(up_clicks, down_clicks, left_clicks, right_clicks, R_val):
    offset_y = 20 + (up_clicks or 0) - (down_clicks or 0)
    offset_x = 150 + (right_clicks or 0) - (left_clicks or 0)
    return challenge_9_code(offset_x, offset_y, R = R_val)
