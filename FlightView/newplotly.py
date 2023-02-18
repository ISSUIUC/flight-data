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
                dict(count=2, label="5m", step="minute", stepmode="backward"),
                dict(count=3, label="10m", step="minute", stepmode="backward"),
                dict(count=4, label="15m", step="minute", stepmode="backward"),
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
