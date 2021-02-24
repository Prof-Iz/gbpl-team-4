import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px


# server_url = ''
# request=Request(server_url)
# response = urlopen(request)
# elevations = response.read()
# data = json.loads(elevations)
# df = pd.json_normalize(data['results'])

data = pd.read_csv(r"C:\Users\User\Desktop\GBPL\gbpl-team-4\IZ\test.csv")


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "GPBL 04"


app.layout = html.Div(
    children=[
        html.Div(
            children=[html.H1(children="💦 🔥 😨", className="header-emoji"),
                      html.H1("Group 4 GPBL", className="header-title"),
                      html.P(
                children=[],
                id="test_stuff",

                className="header-description"
            ), ],
            className="header"),
        html.Div(children=[
            html.Div(children=[
                html.Div(children="Type", className="menu-title"),
                dcc.Dropdown(
                    id="type-filter",
                    options=[
                        {"label": "Temperature", "value": "temp"},
                        {"label": "Humidity", "value": "humidity"},
                    ],
                    value="temp",
                    clearable=False,
                    className="dropdown"
                ),
            ],),
            html.Div(children=[
                html.Div(children="How Many Records", className="menu-title"),
                dcc.Slider(
                    id="records",
                    className="dropdown",
                    min=2,
                    max=300,
                    step=1,
                    value=100,
                ),
            ],),
        ], className="menu"),
        html.Div(
            children=dcc.Graph(id="main-display", figure={}),
            className="card"),
    ],
    className="wrapper",
)


@app.callback(
    [Output("test_stuff", "children"), Output("main-display", "figure")],
    [
        Input("type-filter", "value"),
        Input("records","drag_value")
    ],
)
def update_graph(data_type,records):
    # dff = data.copy()
    main_display_figure = px.line(data, x=np.arange(
        1, data[data_type][:records].count()+1), y=data[data_type][:records], title=data_type)

    dash_update = [f"The Dash is now showing the {data_type} Readings"]
    return dash_update, main_display_figure


if __name__ == "__main__":
    app.run_server(debug=True)
