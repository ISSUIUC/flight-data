import plotly.express as px
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import streamlit as st


# # Read JSON file
# df = pd.read_json("input_file.json")

# # Write to CSV file
# df.to_csv("output_file.csv", index=False)

# Read the dataset from the URL
data = pd.read_csv("FlightView/flightcomputer.csv")

# Create a list to store the line plots for each column
plots = []
data["timestamp_ms"] = data["timestamp_ms"] -  1945435
# Loop through each column in the dataset
for col in data.columns:
    # Convert the Series object to a list
    y_values = data[col].tolist()
    # Create a line plot for the current column
    line_plot = dict(x=data["timestamp_ms"], y=y_values, type="scatter", mode="lines", name=col,
                     hovertemplate="%{y:.2f}")
    # Add the line plot to the plots list
    plots.append(line_plot)


# Create a figure with the line plots
fig = go.Figure(data=plots, layout=dict(title="Flight Data"))

# Update legend and graph font color to white
fig.update_layout(
    legend=dict(
        font=dict(color="white")
    ),
    font=dict(color="white")
)

# Add range slider to the figure
fig["layout"]["xaxis"] = dict(
    rangeselector=dict(),
    rangeslider=dict(visible=True),
    tickformat="%H:%M:%S.%L", # Set the tick format to display the timestamp values as hour:minute:second.millisecond
)

# Set the background color to black
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black'
)
fig.update_layout(height=800, width=1200, margin=dict(l=50, r=50, t=50, b=50))

# Create a table with the max and min values for each column
table = html.Table(
    [html.Tr([html.Th(col), html.Th("Max"), html.Th("Min")], style={'color': 'white'})] +
    [html.Tr([html.Td(col), html.Td(data[col].max()), html.Td(data[col].min())], style={'color': 'white'}) for col in data.columns],
    style={
        'color': 'white'
    }
)

st.plotly_chart(fig, theme = None)

"""
# Define the app
app = dash.Dash(__name__)
image_url1 = 'https://raw.githubusercontent.com/ISSUIUC/flight-data/FligthView-Bug/FlightView/iss%20logo.png'
image_url2 = 'https://raw.githubusercontent.com/ISSUIUC/flight-data/FligthView-Bug/FlightView/flight_view_logo.jpeg'

# Define the layout of the app
app.layout = html.Div(
    style={
        'backgroundColor': 'black'
    }, children=[
    html.Img(src=image_url1, style={'height': '150px', 'width': '150px'}),
    html.Img(src=image_url2, style={'height': '150px', 'width': '450px'}),
    dcc.Tabs([    dcc.Tab(label='Plot', children=[        dcc.Graph(figure=fig, config={'displayModeBar': False})
    ], style={'backgroundColor': 'black', 'color': 'white'}),
    dcc.Tab(label='Table', children=[        table    ], style={'backgroundColor': 'black', 'color': 'white'})
], style={'backgroundColor': 'black'})

])

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
"""