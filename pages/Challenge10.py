import dash
from dash import html, dcc, Output, Input
import numpy as np
from PIL import Image
import plotly.graph_objects as go

def challenge_10_code(offset_x, offset_y, fov, R=75, step=1):

    img = Image.open("test20.png").convert("RGB").resize((100, 100))
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

    fig.add_trace(go.Scattergl(
        x=x_pix,
        y=y_pix,
        mode='markers',
        marker=dict(color=color_strings, symbol="square", size=4, opacity=0.7),
        name='Original Object'
    ))

    k = 0.25
    r_pix = (y_pix - y_pix.min()) / (y_pix.max() - y_pix.min()) + k

    theta_range = np.radians(fov)
    theta = (x_pix / x_pix.max()) * theta_range

    X_img = R * r_pix * np.sin(theta)
    Y_img = R * r_pix * np.cos(theta)

    fig.add_trace(go.Scattergl(
        x=X_img,
        y=Y_img,
        mode='markers',
        marker=dict(color=color_strings, symbol='square', size=10, opacity=0.5),
        name='Anamorphic Projection'
    ))
    
    fig.update_layout(
        title=f"Thin lens: R={R}px, FOV={fov}°",
        xaxis=dict(scaleanchor="y", range=[-190, 190]),
        yaxis=dict(range=[-100, 200]),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig

dash.register_page(__name__, path='/challenge10', name="Challenge 10", order=10)

layout = html.Div([
    html.Div([
        html.Button('up', id='up-nclicks', n_clicks=0),
        html.Button('down', id='down-nclicks', n_clicks=0),
        html.Button('left', id='left-nclicks', n_clicks=0),
        html.Button('right', id='right-nclicks', n_clicks=0),
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Label("Radius: "),
        dcc.Input(id="R", type="number", placeholder="Radius", value=75),
        html.Br(),
        html.Label("Field Of View: "),
        dcc.Slider(id='fov', min=1, max=180, step=0.1, value=10,
                   marks={num: f'{num}°' for num in range(10,180,10)}),
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.H1("Challenge 10"),
        dcc.Graph(id="c10")
    ])
])

@dash.callback(
    Output('c10', 'figure'),
    Input('up-nclicks', 'n_clicks'),
    Input('down-nclicks', 'n_clicks'),
    Input('left-nclicks', 'n_clicks'),
    Input('right-nclicks', 'n_clicks'),
    Input('R', 'value'),
    Input('fov', 'value')
)
def update_figure(up_clicks, down_clicks, left_clicks, right_clicks, R_val, fov_val):
    offset_y = (up_clicks or 0) - (down_clicks or 0)
    offset_x = (right_clicks or 0) - (left_clicks or 0)
    return challenge_10_code(offset_x, offset_y, fov_val, R=R_val)