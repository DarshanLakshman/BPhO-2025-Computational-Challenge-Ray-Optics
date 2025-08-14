import dash
from dash import html

dash.register_page(__name__, path='/', name="Home", order=0)

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1("BPhO Computational Challenge 2025 - Ray Optics"),
                html.Br(),
                html.H2("By Darshan Lakshman and Akshith Arvind")
            ],
            style={"marginBottom": "20px"}
        ),

        html.Div(
            [
                html.H3("⚠ Performance Notice", style={"marginBottom": "10px"}),
                html.P(
                    "Animations on this website may be slow, as this is hosted on a free service. "
                    "Please wait a few seconds for the animations to update, and check if the page is "
                    "‘Updating…’ by looking at the browser tab."
                ),
                html.P(
                    [
                        "For faster render times, please download the code from the ",
                        html.A(
                            "GitHub repo",
                            href="https://github.com/DarshanLakshman/BPhO-2025-Computational-Challenge-Ray-Optics",
                            target="_blank",
                            style={"color": "#0d6efd", "textDecoration": "none"}
                        ),
                        ". Click the 'Code' button, download the ZIP file, and extract it. "
                        "To run locally, open app.py and change `app.run_server` to `app.run`."
                    ]
                )
            ],
            style={
                "backgroundColor": "#fff3cd",  
                "color": "#856404",            
                "border": "1px solid #ffeeba",
                "padding": "15px 20px",
                "borderRadius": "8px",
                "boxShadow": "0px 0px 10px rgba(0,0,0,0.1)"
            }
        )
    ],
    style={"padding": "20px"}
)
