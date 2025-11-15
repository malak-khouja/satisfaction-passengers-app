import dash
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import requests

app= Dash(__name__)
response = requests.get("http://127.0.0.1:8000/passengers/")
data = response.json()
df = pd.DataFrame(data)
fig = px.histogram(df, x="predicted_satisfaction", title="Répartition de la satisfaction")
app.layout = html.Div([
    html.H1("Dashboard Satisfaction Passagers"),
    dcc.Graph(figure=fig)
])


if __name__ == "__main__":
    app.run(debug=True)