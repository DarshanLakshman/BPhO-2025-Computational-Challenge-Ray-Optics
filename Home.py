import dash
from dash import html

dash.register_page(__name__, path='/', name = "Home", order = 0)

layout = html.Div(
    children=[
        html.Div(children = [
            html.H1("BPhO Computational Challenge 2025 - Ray Optics"),
            html.Br(),
            html.H2("By Darshan and Akshith")
        ]
        )
    ]
)