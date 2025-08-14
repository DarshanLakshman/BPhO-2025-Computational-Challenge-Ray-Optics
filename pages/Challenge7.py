import dash
from dash import html, dcc, Output, Input
import numpy as np
from PIL import Image
import plotly.graph_objects as go

def challenge_7_code(offset_x, offset_y, f_val=20, step=1):

    img = Image.open("test20.png").convert("RGB").resize((20, 20))
    data = np.array(img)
    h, w, _ = data.shape

    yy, xx = np.mgrid[0:h, 0:w]
    xs = xx.flatten().astype(float)
    ys = yy.flatten().astype(float)

    x_pix = (xs - w / 2 + offset_x * step) * (20 / w)
    y_pix = ((h - ys) - h / 2 + offset_y * step) * (20 / h)

    colors = data.reshape(-1, 3)
    color_strings = np.array([f'rgb({r},{g},{b})' for r, g, b in colors])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, 0],
        y=[-100, 100],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Lens axis'
    ))

    fig.add_trace(go.Scattergl(
        x=x_pix,
        y=y_pix,
        mode='markers',
        marker=dict(color=color_strings, symbol="square", size=4, opacity=0.7),
        name='Object'
    ))

    mask =  (0 < x_pix) & (x_pix < f_val)
    X_img = np.full_like(x_pix, np.nan, dtype=float)
    Y_img = np.full_like(y_pix, np.nan, dtype=float)

    X_img[mask] = -f_val * (x_pix[mask]) / (x_pix[mask] - f_val)
    Y_img[mask] = (y_pix[mask] / x_pix[mask]) * X_img[mask]


    fig.add_trace(go.Scattergl(
        x=X_img,
        y=Y_img,
        mode='markers',
        marker=dict(color=color_strings, symbol="square", size=8.7, opacity=0.7)
    ))

    fig.update_layout(
        title=f"Thin lens: f={f_val}px ",
        xaxis=dict(scaleanchor="y", range=[-75, 190]),
        yaxis=dict(range=[-100, 100]),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig

dash.register_page(__name__, path='/challenge7', name="Challenge 7", order=7)

layout = html.Div([
    html.Div([
        html.Button('up', id='up-nclicks', n_clicks=0),
        html.Button('down', id='down-nclicks', n_clicks=0),
        html.Button('left', id='left-nclicks', n_clicks=0),
        html.Button('right', id='right-nclicks', n_clicks=0),
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Label("Focal Length (f) in px:  "),
        dcc.Input(id="f_val", type="number", placeholder="focal length (pixels)", value=100)
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.H1("Challenge 7"),
        dcc.Graph(id="c7")
    ])
])

@dash.callback(
    Output('c7', 'figure'),
    Input('up-nclicks', 'n_clicks'),
    Input('down-nclicks', 'n_clicks'),
    Input('left-nclicks', 'n_clicks'),
    Input('right-nclicks', 'n_clicks'),
    Input('f_val', 'value')
)
def update_figure(up_clicks, down_clicks, left_clicks, right_clicks, f_val):
    offset_y = (up_clicks or 0) - (down_clicks or 0)
    offset_x = 50 + (right_clicks or 0) - (left_clicks or 0)
    return challenge_7_code(offset_x, offset_y, f_val=f_val)
