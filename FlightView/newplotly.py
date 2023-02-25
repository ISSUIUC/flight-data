import plotly.express as px
import pandas as pd
import plotly.io as pio

# Read the dataset from the URL
data = pd.read_csv("https://raw.githubusercontent.com/ISSUIUC/flight-data/master/20221029/flight_computer.csv")

# Create a list to store the line plots for each column
plots = []

# Loop through each column in the dataset
for col in data.columns:
    # Convert the Series object to a list
    y_values = data[col].tolist()
    # Create a line plot for the current column
    line_plot = dict(x=data["timestamp_ms"], y=y_values, type="scatter", mode="lines", name=col)
    # Add the line plot to the plots list
    plots.append(line_plot)

# Create a figure with the line plots
fig = dict(data=plots, layout=dict(title="Flight Data"))

# Add range slider to the figure
fig["layout"]["xaxis"] = dict(
    rangeselector=dict(
        buttons=list(
            [
                dict(count=2, label="2m", step="minute", stepmode="backward"),
                dict(count=3, label="3m", step="minute", stepmode="backward"),
                dict(count=4, label="4m", step="minute", stepmode="backward"),
                dict(step="all"),
            ]
        )
    ),
    rangeslider=dict(visible=True),
    type="date",
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

image_url1 = 'https://raw.githubusercontent.com/ISSUIUC/flight-data/FligthView-Bug/FlightView/307314995_392750989713187_3386142925000647721_n-removebg-preview.png'
image_tag1 = f'<img src="{image_url1}" width="200" height="175">'
image_url2 = 'https://raw.githubusercontent.com/ISSUIUC/flight-data/FligthView-Bug/FlightView/flight_view_logo.jpeg'
image_tag2 = f'<img src="{image_url2}" width="500" height="175">'

# Set the background color to black
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black'
)


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