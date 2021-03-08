import pyrebase
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
# import json
# import numpy as np
from dash.dependencies import Output, Input
import plotly.graph_objs as go
# import plotly.express as px
from collections import deque

firebaseConfig = {
    "apiKey": "AIzaSyBbo4ZGJwHpdDMsElUZgstbXET-R3VIkO4",
    "authDomain": "gpbl-team-04.firebaseapp.com",
    "databaseURL": "https://gpbl-team-04-default-rtdb.firebaseio.com",
    "projectId": "gpbl-team-04",
    "storageBucket": "gpbl-team-04.appspot.com",
    "messagingSenderId": "364991924559",
    "appId": "1:364991924559:web:d3e98858b57a7d39211d3a",
    "measurementId": "G-NB1JG0ZZ2D"
}

firebase = pyrebase.initialize_app(config=firebaseConfig)

email = "iz@test.com"
password = "password"

auth = firebase.auth()

user = auth.sign_in_with_email_and_password(email, password)

db = firebase.database()

X = deque(maxlen=5)
Y1 = deque(maxlen=5)
Y2 = deque(maxlen=5)
XD = [1]
Y1D = [1]
Y2D = [1]
X.append(1)
Y1.append(1)
Y2.append(1)

warehouse_info = db.child("warehouse/").get(token=user['idToken'])
prev_warehouse = ''
prev_sensor = ''

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
                html.Div(children="Warehouse", className="menu-title"),
                dcc.Dropdown(
                    id="type-filter",
                    options=[{"label": warehouse.key(), "value": warehouse.key()} for warehouse in warehouse_info.each()
                             ],
                    value="",
                    clearable=False,
                    className="dropdown"
                ),
            ],
            ),
            html.Div(children=[
                html.Div(children="Sensor", className="menu-title"),
                dcc.Dropdown(
                    id="sensor-filter",
                    value="",
                    options=[],
                    # clearable=False,
                    className="dropdown"
                ),
            ],
            ),
        ], className="menu"),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(id="temp-display"),
                    className="card"),
                html.Div(
                    children=dcc.Graph(id="humidity-display"),
                    className="card"),
                dcc.Interval(interval=2000, n_intervals=0, id='time_interval')]),
        # dcc.Interval(interval=600000, n_intervals=0, id='refresh_auth')
    ],

    className="wrapper",
)


@app.callback(
    [Output("test_stuff", "children"),
     Output("temp-display", "figure"),
     Output("humidity-display", "figure")],
    [
        Input('time_interval', "n_intervals"),
        Input('sensor-filter', "value"),
        Input('type-filter', 'value'),

    ],
)
def update_graph(n, sensor, warehouse):
    global prev_warehouse
    global prev_sensor
    date_mode = True
    search = True
    global XD
    global Y1D
    global Y2D

    if not date_mode:
        if sensor != prev_sensor or warehouse != prev_warehouse:
            X.clear()
            Y1.clear()
            Y2.clear()
            X.append(1)
            Y1.append(1)
            Y2.append(1)
            prev_warehouse = warehouse
            prev_sensor = sensor

        elif sensor != '' and warehouse != '':
            try:
                print("Database accessed")
                readings = db.child(f"{warehouse}/{sensor}/").order_by_key().limit_to_last(1).get(token=user['idToken'])
                for reading in readings.each():
                    stamp = pd.Timestamp(float(reading.key()), unit='s')
                    if stamp != X[-1]:
                        X.append(stamp)
                        temp = reading.val()
                        Y1.append(temp["temp"])
                        Y2.append(temp["humidity"])

                prev_warehouse = warehouse
                prev_sensor = sensor

            except Exception as e:
                print(e)

        graph_temp_data = go.Scatter(x=list(X), y=list(Y1), name="temperature", mode="lines+markers")
        graph_humidity_data = go.Scatter(x=list(X), y=list(Y2), name="humidity", mode="lines+markers")
        graph_temp = go.Figure(data=graph_temp_data,
                               layout=go.Layout(xaxis=dict(range=[X[0], X[-1]]),
                                                yaxis=dict(range=[min(Y1) - 1, min(Y1) + 1]), title=f"Temperature Readings {warehouse}- Sensor:{sensor}",
                                                transition={'duration': 1000, 'easing': 'cubic-in-out'}))

        graph_humidity = go.Figure(data=graph_humidity_data,
                                   layout=go.Layout(xaxis=dict(range=[X[0], X[-1]]),
                                                    yaxis=dict(range=[min(Y2) - 1, max(Y2) + 1]),
                                                    title=f"Humidity Readings {warehouse}- Sensor: {sensor}",
                                                    transition={'duration': 1000, 'easing': 'cubic-in-out'}))

        dash_update = [f"The Dash is now showing the Readings at {X[-1]}"]

    elif search and date_mode:
        if sensor != prev_sensor or warehouse != prev_warehouse:

            prev_warehouse = warehouse
            prev_sensor = sensor
            try:
                XD = []
                Y1D = []
                Y2D = []
                print("Database accessed")
                readings = db.child(f"{warehouse}/{sensor}/").order_by_key().get(
                    token=user['idToken'])
                for reading in readings.each():
                    stamp = pd.Timestamp(float(reading.key()), unit='s')
                    XD.append(stamp)
                    temp = reading.val()
                    Y1D.append(temp["temp"])
                    Y2D.append(temp["humidity"])

            except Exception as e:
                print(e)
                XD = [1]
                Y1D = [1]
                Y2D = [1]

        graph_temp_data = go.Scatter(x=list(XD), y=list(Y1D), name="temperature", mode="lines+markers")
        graph_humidity_data = go.Scatter(x=list(XD), y=list(Y2D), name="humidity", mode="lines+markers")
        title = f"Temperature Readings {warehouse}- Sensor: {sensor}"
        graph_temp = go.Figure(data=graph_temp_data,
                               layout=go.Layout(xaxis=dict(range=[XD[0], XD[-1]]),
                                                yaxis=dict(range=[min(Y1D) - 1, min(Y1D) + 1]), title=title,
                                                transition={'duration': 1000, 'easing': 'cubic-in-out'}))

        graph_humidity = go.Figure(data=graph_humidity_data,
                                   layout=go.Layout(xaxis=dict(range=[XD[0], XD[-1]]),
                                                    yaxis=dict(range=[min(Y2D) - 1, max(Y2D) + 1]),
                                                    title=f"Humidity Readings {warehouse}- Sensor:{sensor}",
                                                    transition={'duration': 1000, 'easing': 'cubic-in-out'}))

        dash_update = [f"The Dash is now showing the Historical Readings for {warehouse} - Sensor: {sensor}"]

    return dash_update, graph_temp, graph_humidity


@app.callback(Output("sensor-filter", "options"),
              Input("type-filter", "value"))
def update_options(selection):
    options = [{"label": x, "value": x} for x in warehouse_info.val()[selection]["esp"]]
    return list(options)


if __name__ == "__main__":
    app.run_server(debug=True)
