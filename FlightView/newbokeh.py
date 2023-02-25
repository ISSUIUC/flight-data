import plotly.express as px
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go

# Read the dataset from the URL
data = pd.read_csv("https://raw.githubusercontent.com/ISSUIUC/flight-data/master/20221029/flight_computer.csv")

# Create a list to store the line plots for each column
plots = []
data["timestamp_ms"] = data["timestamp_ms"] - 1945435
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

# Export the figure as JavaScript
js_code = pio.to_json(fig)

# Print the JavaScript code
print(js_code)

with open("my_plot.json", "w") as f:
    f.write(js_code)

# Convert the JSON to a Plotly figure object
fig = pio.from_json(js_code)

# Write the figure to an HTML file
pio.write_html(fig, 'plotly_figure.html')

# Add image and heading to HTML file
with open('plotly_figure.html', 'r') as f:
    html_content = f.read()

image_url1 = 'https://raw.githubusercontent.com/ISSUIUC/flight-data/FligthView-Bug/FlightView/iss%20logo.png'
image_tag1 = f'<img src="{image_url1}" width="200" height="175">'
image_url2 = 'https://raw.githubusercontent.com/ISSUIUC/flight-data/FligthView-Bug/FlightView/flight_view_logo.jpeg'
image_tag2 = f'<img src="{image_url2}" width="500" height="175">'

# Set the FlightView title
new_html_content = f'''
<html>
<head>
    <title>FlightView</title>
    <style>
        body {{
            background-color: black;
        }}
        h1 {{
            font-family: 'Exo', sans-serif;
            color: red;
        }}
    </style>
</head>
<body>
    {image_tag1}
    {image_tag2}
    {html_content}
</body>
</html>
'''

# Write the modified HTML file
with open('plotly_figure.html', 'w') as f:
    f.write(new_html_content)
