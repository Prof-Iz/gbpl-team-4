import pyrebase
import pandas as pd
import plotly.express as px

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

_email = "iz@test.com"
_password = "password"

auth = firebase.auth()

user = auth.sign_in_with_email_and_password(_email, _password)

db = firebase.database()

readings = db.child("MAL01/iz/data/2021-03-01").get(token=user['idToken'])

df = pd.DataFrame()

for reading in readings.each():
    to_append = [pd.Timestamp(reading.key())]
    temp = reading.val()
    to_append.append(float(temp["temp"]))
    to_append.append((temp["humidity"]))
    to_append = pd.Series(to_append)
    df = df.append(to_append, ignore_index=True)


graph = px.line(df, x=0, y=[1], range_y=[20.0, 45.0])
graph.show()
