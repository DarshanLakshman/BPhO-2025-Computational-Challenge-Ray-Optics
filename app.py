from dash import Dash, html, dcc
import dash

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css)
server= app.server

img_tag = html.Img(src="assets/cc.png", width=27, className="m-1")
pages_links = [dcc.Link(page['name'], href=page["relative_path"], className="nav-link")\
	         for page in dash.page_registry.values()]

app.layout = html.Div([

    html.Nav(children=[
	    html.Div([
			    html.Div([ ] + pages_links, className="navbar-nav")
        ], className="container-fluid"),
    ], className="navbar navbar-expand-lg bg-dark", **{"data-bs-theme": "dark"}),

    html.Div([
	    html.Br(),
	    dash.page_container
	], className="col-6 mx-auto")
], style={"height": "1000vh", "background-color": "#e3f2fd"})

if __name__ == '__main__':
	app.run_server(debug=True)
