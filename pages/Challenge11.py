import dash
from dash import html, dcc, Output, Input
import numpy as np
import plotly.graph_objects as go
from helpers import get_colour

def challenge_11a_code(deg_x_start = 0, deg_y_start = 0, deg_x_end = 90, deg_y_end = 90):
    fig = go.Figure()

    for f in [4.38e14, 4.96e14, 5.17e14, 5.63e14, 6.35e14, 6.85e14, 7.45e14]:
        n = ((1 / (1.731 - 0.261 * (f / 10 ** 15) ** 2)) ** 0.5 + 1) ** 0.5
        t = np.linspace(0, np.pi / 2 - 0.01, 1000)
        e = np.pi - 6 * np.arcsin(np.sin(t) / n) + 2 * t
        e1 = 4 * np.arcsin(np.sin(t) / n) - 2 * t
        r, g, b = get_colour(f)
        colour_string = f"rgb({r*256}, {g*256}, {b*256})"

        fig.add_trace(go.Scatter(
            x=np.rad2deg(t),
            y=np.rad2deg(e),
            mode='lines',
            line=dict(color=colour_string, width=1),
        ))

        fig.add_trace(go.Scatter(
            x=np.rad2deg(t),
            y=np.rad2deg(e1),
            mode='lines',
            line=dict(color=colour_string),
        ))

    fig.update_layout(
        title = "Elevation of Deflected Beam",
        xaxis=dict(range=[deg_x_start, deg_x_end]),
        yaxis=dict(range=[deg_y_start, deg_y_end]),
        template="plotly_white",
        showlegend=False
    )

    return fig


def challenge_11b_code():
    fig = go.Figure()

    f = np.linspace(400 * 10 ** 12, 800 * 10 ** 12, 1000) 
    n = ((1 / (1.731 - 0.261 * (f / 10 ** 15) ** 2)) ** 0.5 + 1) ** 0.5

    t = np.arcsin(np.clip((4 - n ** 2 / 3) ** 0.5, -1, 1))
    e = 4 * np.arcsin(np.sin(t) / n) - 2 * t

    t1 = np.arcsin(np.clip(((9 - n ** 2) / 8) ** 0.5, -1, 1))
    e1 = np.pi - 6 * np.arcsin(np.sin(t1) / n) + 2 * t1

    c = [get_colour(float(x)) for x in f]
    c_strs = [f'rgb({r*255},{g*255},{b*255})' for r, g, b in c]

    fig.add_trace(go.Scatter(
        x=f,
        y=np.rad2deg(e),
        mode='markers',
        marker=dict(color=c_strs, size=5),
    ))

    fig.add_trace(go.Scatter(
        x=f,
        y=np.rad2deg(e1),
        mode='markers',
        marker=dict(color=c_strs, size=5),
    ))

    fig.update_layout(
        title = "Elevation of single and double rainbows",
        xaxis_title = "Frequency/Hz",
        yaxis_title = "Elevation/deg",
        showlegend = False
    )

    return fig

def challenge_11c_code():
    
    fig = go.Figure()

    f = np.linspace(400 * 10 ** 12, 800 * 10 ** 12, 1000)
    n = ((1 / (1.731 - 0.261 * (f / 10 ** 15) ** 2)) ** 0.5 + 1) ** 0.5
    t1 = np.arcsin(np.clip(np.sqrt((9 - n ** 2) / 8), -1, 1))
    t2 = np.arcsin(np.clip(np.sqrt((4 - n ** 2) / 3), -1, 1))
    e1 = np.pi - 6 * np.arcsin(np.sin(t1) / n) + 2 * t1
    e2 = 4 * np.arcsin(np.sin(t1) / n) - 2 * t1
    p1 = (e1 - 2 * t1 - np.pi) / -6
    p2 = (e1 - 2 * t2 - np.pi) / -6
    colours = [get_colour(fr) for fr in f]
    colour_strings =  [f'rgb({r*255},{g*255},{b*255})' for r, g, b in colours]

    fig.add_trace(go.Scatter(
        x=f,
        y=np.rad2deg(p1),
        mode='markers',
        marker=dict(color=colour_strings, size=5),
    ))

    fig.add_trace(go.Scatter(
        x=f,
        y=np.rad2deg(p2),
        mode='markers',
        marker=dict(color=colour_strings, size=5),
    ))


    t1 = np.arcsin(np.clip(n, -1, 1))
    e1 = np.pi - 6 * np.arcsin(np.sin(t1) / n) + 2 * t1
    crit_ang = (e1 - 2 * t1 - np.pi) / -6
    colours = [get_colour(fr) for fr in f]
    colour_strings =  [f'rgb({r*255},{g*255},{b*255})' for r, g, b in colours]



    fig.add_trace(go.Scatter(
        x=f,
        y=np.rad2deg(crit_ang),
        mode='markers',
        marker=dict(color ="black", size=2),
    ))

    fig.update_layout(
        title = "Refraction angle of single and double rainbows",
        showlegend = False
    )

    

    return fig

def challenge_11d_code(alpha):

    fig = go.Figure()

    h, r = 0, 10
    alpha = np.radians(alpha)

    for f in [4.38e14, 4.96e14, 5.17e14, 5.63e14, 6.35e14, 6.85e14, 7.45e14]:
        n = ((1 / (1.731 - 0.261 * (f / 10 ** 15) ** 2)) ** 0.5 + 1) ** 0.5
        t_primary = np.arcsin(np.sqrt((4 - n ** 2) / 3))
        t_secondary = np.arcsin(np.sqrt((9 - n ** 2) / 8))
        e_primary = 4 * np.arcsin(np.sin(t_primary) / n) - 2 * t_primary
        e_secondary = np.pi - 6 * np.arcsin(np.sin(t_secondary) / n) + 2 * t_secondary
        r_primary = r * np.sin(e_primary) * np.cos(alpha)
        r_secondary = r * np.sin(e_secondary) * np.cos(alpha)
        horizon = r * np.sin(e_primary) * np.cos(alpha) - r * np.sin(e_primary - alpha) - h
        beta = np.linspace(0, 2 * np.pi, 1000)
        primary_x, primary_y = r_primary * np.cos(beta), r_primary * np.sin(beta)
        secondary_x, secondary_y = r_secondary * np.cos(beta), r_secondary * np.sin(beta)
        mask = primary_y > horizon
        mask1 = secondary_y > horizon
        cr,cg,cb = get_colour(f)
        colour_string = f"rgb({(cr*255)}, {(cg*255)}, {(cb*255)})"

        fig.add_trace(go.Scatter(
            x=primary_x[mask],
            y=primary_y[mask],
            mode='lines',
            line=dict(color=colour_string)
        ))

        fig.add_trace(go.Scatter(
            x=secondary_x[mask1],
            y=secondary_y[mask1],
            mode='lines',
            line=dict(color=colour_string)
        ))

        fig.add_trace(go.Scatter(
            x=np.linspace(-r, r, 1000),
            y=[horizon for _ in range(1000)],
            mode='lines',
            line=dict(color='rgb(0,255,0)')
        ))

    fig.update_layout(
        title = f"Primary and Seconday Rainbow Model (α = {np.degrees(alpha):3f})",
        showlegend=False,
        template="plotly_white"
    )

    return fig


dash.register_page(__name__, path='/challenge11', name="Challenge 11", order=11)

layout = html.Div([

    html.Div([
        html.H1("Challenge 11")
    ]),

    html.Div([
        dcc.Graph(id="c11-a",  figure = challenge_11a_code()),
    ],style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id="c11-a",  figure = challenge_11a_code(40,40,90,60))
    ],style={'width': '48%', 'display': 'inline-block', 'float':'right'}),

    html.Div([
        html.Br(),
        dcc.Graph(id="c11-b", figure = challenge_11b_code()),
        html.Br()
    ]),

    html.Div([
        html.Br(),
        dcc.Graph(id="c11-c", figure = challenge_11c_code())
    ]),

    html.Div([
        html.Br(),
        html.Label("Solar Angle Alpha (α)"),
        dcc.Slider(id='slider-alpha', min=0.1, max=45, step=0.1, value=10, 
                   marks={0.1: '0.1°', 10: '10°', 20: '20°', 30: '30°',40: '40°'}),
        dcc.Graph(id="c11-d")
    ])
])

@dash.callback(
    Output('c11-d', 'figure'),
    Input('slider-alpha', 'value'),
)
def update(alpha):
    return challenge_11d_code(alpha)