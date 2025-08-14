import dash
from dash import html, dcc, Output, Input
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from helpers import get_colour

def n_calc(frequency):
    c = 3e8 
    wavelength = c / (frequency) * 1e9  
    x = wavelength / 1000.0

    a = np.array([1.03961212, 0.231792344, 1.01146945])
    b = np.array([0.00600069867, 0.0200179144, 103.560653])

    y = np.zeros_like(x, dtype=float)
    for k in range(len(a)):
        y += (a[k] * x**2) / (x**2 - b[k])

    n = np.sqrt(1 + y)
    return n

def intersect_ray_calc(P, theta, A, C):
    Px, Py = P
    Ax, Ay = A
    Cx, Cy = C

    dx, dy = np.cos(theta), np.sin(theta)  
    ex, ey = Cx - Ax, Cy - Ay      

    denom = dx * ey - dy * ex

    t = ((Ax - Px) * ey - (Ay - Py) * ex) / denom
    intersection = (Px + t * dx, Py + t * dy)
    return intersection

def challenge_12_code(theta_i, alpha):
    fig = go.Figure()

    n_a = 1.0003

    alpha = np.radians(alpha)
    theta_i = np.radians(theta_i)

    a = 1 * np.sin(alpha * 0.5)  
    h = 1 * np.cos(alpha * 0.5)
    A, B, C = (0.0, h), (-a, 0.0), (a, 0.0)

    fig.add_trace(
        go.Scatter(
            x=[B[0], C[0], A[0], B[0]],
            y=[B[1], C[1], A[1], B[1]],
            mode="lines",
            fill="toself",     
            line=dict(color="white"),
            name="Prism"
        )
    )

    light_hit_pt = (-a/2, h/2)

    slope = (A[1] - B[1]) / (A[0] - B[0])
    normal_slope = -1 / slope
    norm_angle = np.arctan(normal_slope)
    

    start_x = light_hit_pt[0] - 2 * np.cos(norm_angle + theta_i)
    start_y = light_hit_pt[1] - 2 * np.sin(norm_angle + theta_i)


    fig.add_trace(go.Scatter(
        x=[start_x, light_hit_pt[0]],
        y=[start_y, light_hit_pt[1]],
        mode="lines",
        line=dict(color="white", width=2),
        name="Incoming ray"
    ))

    fig.add_trace(go.Scatter(
        x=[light_hit_pt[0] - 0.1 * np.cos(norm_angle),
        light_hit_pt[0] + 0.1 * np.cos(norm_angle) ],

        y=[light_hit_pt[1] - 0.1 * np.sin(norm_angle),  
            light_hit_pt[1] + 0.1 * np.sin(norm_angle) ],
        mode="lines",
        line=dict(color="green", dash="dot"),
        name="Normal"
    ))

    frequencies = np.linspace(405e12 , 790e12, 50).tolist()

    for f in frequencies:

        n_g_color = n_calc(f)
        cr, cb, cg = get_colour(f)
        color_str = f"rgb({cr*256},{cb*256},{cg*256})"

        theta_t = np.arcsin(np.sqrt(n_g_color**2 - np.sin(theta_i)**2) * np.sin(alpha) - np.sin(theta_i) * np.cos(alpha))
        delta = theta_i + theta_t - alpha
        beta = norm_angle + np.arcsin(n_a * np.sin(theta_i)/n_g_color)
        secondary_ray_end_x, secondary_ray_end_y = intersect_ray_calc(light_hit_pt, beta, A, C)

        fig.add_trace(go.Scatter(
            x=[light_hit_pt[0], secondary_ray_end_x],
            y=[light_hit_pt[1], secondary_ray_end_y],
            mode="lines",
            line=dict(color=color_str, width=2),
            name="Seconday ray"
        ))

        fig.add_trace(go.Scatter(
            x=[secondary_ray_end_x - 0.1 * np.cos(-norm_angle),
            secondary_ray_end_x + 0.1 * np.cos(-norm_angle) ],

            y=[secondary_ray_end_y - 0.1 * np.sin(-norm_angle),  
                secondary_ray_end_y + 0.1 * np.sin(-norm_angle) ],
            mode="lines",
            line=dict(color="green", dash="dot"),
            name="Normal 2"
        ))

        emergent_angle = -norm_angle - theta_t
        emergent_x, emergent_y = secondary_ray_end_x + 1 * np.cos(emergent_angle), secondary_ray_end_y + 1 * np.sin(emergent_angle)
        fig.add_trace(go.Scatter(
            x=[secondary_ray_end_x, emergent_x],
            y=[secondary_ray_end_y, emergent_y],
            mode="lines",
            line=dict(color=color_str, width=2),
            name="Emergent ray"
        ))
        

        
    fig.update_layout(
        title=f'Prism Dispersion Model, α = {np.degrees(alpha):3f}, θᵢ = {np.degrees(theta_i):3f}',
        template='plotly_dark',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        autosize=True,
        showlegend=False
    )


    return fig


def challenge_12b_code(f, alpha):

    n = n_calc(f)
    
    theta_i_deg = np.linspace(0, 90, 500)
    theta_i = np.radians(theta_i_deg) 

    arg = np.sqrt(n**2 - np.sin(theta_i)**2) * np.sin(alpha) - np.sin(theta_i) * np.cos(alpha)
    theta_t = np.arcsin(arg)
    
    theta_t_deg = np.degrees(theta_t)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=theta_i_deg, y=theta_t_deg, mode='lines', name='theta_t vs theta_i'))

    fig.update_layout(
        title='Theta_t vs Theta_i',
        xaxis_title='Theta_i (degrees)',
        yaxis_title='Theta_t (degrees)',
        template='plotly_white'
    )

    return fig

def challenge_12c_code(f, alpha):

    n = n_calc(f)
    
    theta_i_deg = np.linspace(0, 90, 500)
    theta_i = np.radians(theta_i_deg) 

    arg = np.sqrt(n**2 - np.sin(theta_i)**2) * np.sin(alpha) - np.sin(theta_i) * np.cos(alpha)
    theta_d = np.arcsin(arg) + theta_i - alpha
    
    d_deg = np.degrees(theta_d)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=theta_i_deg, y=d_deg, mode='lines', name='theta_t vs theta_i'))

    fig.update_layout(
        title='delta vs Theta_i',
        xaxis_title='Theta_i (degrees)',
        yaxis_title='Theta_t (degrees)',
        template='plotly_white'
    )

    return fig

def challenge_12d_code(f):
    n = n_calc(f)
    
    fig = go.Figure()  
    
    for alpha in range(10, 90, 10):
        theta_i_deg = np.linspace(0, 90, 500)
        theta_i = np.radians(theta_i_deg) 

        arg = np.sqrt(n**2 - np.sin(theta_i)**2) * np.sin(np.radians(alpha)) - np.sin(theta_i) * np.cos(np.radians(alpha))
        theta_d = np.arcsin(arg) + theta_i - np.radians(alpha)
        
        d_deg = np.degrees(theta_d)

        fig.add_trace(go.Scatter(
            x=theta_i_deg,
            y=d_deg,
            mode='lines',
            name=f'alpha = {alpha}°'
        ))

    fig.update_layout(
        title='delta vs Theta_i for multiple alphas',
        xaxis_title='Theta_i (degrees)',
        yaxis_title='d (degrees)',
        template='plotly_white'
    )

    return fig
    

dash.register_page(__name__, path='/challange12', name="Challenge 12", order=12)

layout = html.Div([
    html.Div([
        html.H1("Challenge 12"), 
        html.Label("Theta_i : "),
        dcc.Slider(id='theta', min=1, max=90, step=0.1, value=7,
                   marks={num: f'{num}°' for num in range(10,90,10)}),
        html.Br(),
        html.Label("Alpha : "),
        dcc.Slider(id='alpha', min=1, max=90, step=0.1, value=45,
                   marks={num: f'{num}°' for num in range(10,90,10)}),
        html.Br(),
    ]), 

    html.Div([
        dcc.Graph(id="prism")
    ]),

    html.Div([
        html.Br()
    ]),

    html.Div([
        html.Label("Alpha (α):"),
        dcc.Slider(id='alpha2', min=1, max=90, step=0.1, value=45,
                   marks={num: f'{num}°' for num in range(10,90,10)}),
        html.Label("Frequency (THz): "),
        html.Br(),
        dcc.Input(id="frequency", type="number", placeholder="frequency in THz", value=542),
        html.Br(),
        html.Br()
    ]),

    html.Div([
        dcc.Graph(id="c12-b-1")
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id="c12-b-2")
    ], style={'width': '48%', 'display': 'inline-block', 'float':'right'}),

    html.Div([
        html.Br()
    ]),

    html.Div([
        dcc.Graph(id="c12-b-3")
    ])
])

@dash.callback(
    Output('prism', 'figure'),
    Input('theta', 'value'),
    Input('alpha', 'value')
)
def update_figure(theta, alpha):

    return challenge_12_code(theta, alpha)


@dash.callback(
    Output('c12-b-1', 'figure'),
    Input('frequency', 'value'),
    Input('alpha2', 'value')
)
def update_figure2(f, alpha):
    return challenge_12b_code(f*10**12, alpha * np.pi/180)

@dash.callback(
    Output('c12-b-2', 'figure'),
    Input('frequency', 'value'),
    Input('alpha2', 'value')
)
def update_figure3(f, alpha):
    return challenge_12c_code(f*10**12, alpha * np.pi/180)

@dash.callback(
    Output('c12-b-3', 'figure'),
    Input('frequency', 'value'),
)
def update_figure4(f):
    return challenge_12d_code(f*10**12)