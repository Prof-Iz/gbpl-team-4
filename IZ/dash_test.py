import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import numpy as np

# server_url = ''
# request=Request(server_url)
# response = urlopen(request)
# elevations = response.read()
# data = json.loads(elevations)
# df = pd.json_normalize(data['results'])

data = pd.read_csv(r"C:\Users\User\Desktop\GBPL\gbpl-team-4\IZ\test.csv")
print(data)


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
        children = [html.H1(children="💦 🔥 😨",className="header-emoji"),
        html.H1("Group 4 GPBL",className="header-title"),
        html.P(
            children="Test Dash Application for our Stuff",
            className="header-description"
        ),],
        className="header"),
        html.Div(
            children = dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": np.arange(1,data["temp"].count()),
                            "y": data["temp"],
                            "type": "lines",
                            "hovertemplate": "%{y:.2f} C",
                        },
                    ],
                    "layout": {"title": "Temperature over time",
                    "colorway": ["#17B897"]},
                },
            ),
            className="card"),
        html.Div(
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": np.arange(1,data["temp"].count()),
                        "y": data["humidity"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Humidity over Time"},
            },
        ),className="card"),
    ], className = "wrapper",
)



if __name__ == "__main__":
    app.run_server(debug=True)