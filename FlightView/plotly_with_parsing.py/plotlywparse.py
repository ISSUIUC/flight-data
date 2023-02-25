import subprocess
import plotly.express as px
import pandas as pd
import plotly.io as pio

# Compile C++ code with clang++
subprocess.run(["clang++", "-std=c++11", "/Users/aadityavoruganti/ISS/FlightaViea/flight-data/parse_data.cpp", "-o", "parse_data"])

# Run the compiled binary and write the output to a temporary file
subprocess.run(["./parse_data", "/Users/aadityavoruganti/ISS/FlightaViea/flight-data/20221029/raw_binary.dat", "temp_parsed_data.csv"])

# Read the temporary parsed data from the output file and filter based on a condition
temp_parsed_data = pd.read_csv("temp_parsed_data.csv")
parsed_data = temp_parsed_data[(temp_parsed_data['rocketState_data.rocketState1'] > 1) & (temp_parsed_data['rocketState_data.rocketState1'] != 0)]

print(parsed_data)

# Create a list to store the line plots for each column
plots = []

# Loop through each column in the dataset
for col in parsed_data.columns:
    # Convert the Series object to a list
    y_values = parsed_data[col].tolist()
    # Create a line plot for the current column
    line_plot = dict(x=parsed_data["gps_data.timeStamp_GPS"], y=y_values, type="scatter", mode="lines", name=col)
    # Add the line plot to the plots list
    plots.append(line_plot)

# Create a figure with the line plots
fig = dict(data=plots, layout=dict(title="Flight Data"))

# Add range slider to the figure
fig["layout"]["xaxis"] = dict(
    rangeselector=dict(
        buttons=list(
            [
                dict(count=30, label="10m", step="minute", stepmode="backward"),
                dict(count=40, label="20m", step="minute", stepmode="backward"),
                dict(count=50, label="30m", step="minute", stepmode="backward"),
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

image_url = 'https://raw.githubusercontent.com/ISSUIUC/flight-data/FligthView-Bug/FlightView/307314995_392750989713187_3386142925000647721_n-removebg-preview.png'
image_tag = f'<img src="{image_url}" width="100" height="88">'

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
    {image_tag}
    <h1>FlightView</h1>
    {html_content}
</body>
</html>
'''

# Write the modified HTML file
with open('plotly_figure.html', 'w') as f:
    f.write(new_html_content)