from bokeh.plotting import figure, show
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Button
from bokeh.io import curdoc
import pandas as pd
from bokeh.palettes import Spectral4
from bokeh.models import CustomJS


#Read the dataset from the URL
data = pd.read_csv("https://raw.githubusercontent.com/ISSUIUC/flight-data/master/20221029/flight_computer.csv")

#Convert the data into a ColumnDataSource for use with bokeh
source = ColumnDataSource(data)

# Create a figure with the range tool
plot = figure(x_range=(data["timestamp_ms"].min(), data["timestamp_ms"].max()), 
              y_range=(data["ax"].min(), data["ax"].max()), 
              width=1200, height=800)

# Create a dictionary to store the line plots for each column
plots = {}

# Use a counter to keep track of which color to use
color_counter = 0

# Loop through each column in the dataset
for col in data.columns:
    # Create a line plot for the current column
    line_plot = plot.line(x="timestamp_ms", y=col, source=source, line_color=Spectral4[color_counter % 4], legend_label=col)
    # Add the line plot to the plots dictionary
    plots[col] = line_plot
    # Set the visibility of the line plot to False
    line_plot.visible = False
    # Increment the color counter
    color_counter += 1

# Add a legend to the plot
plot.legend.location = "top_left"
plot.legend.click_policy="hide"

# Create a list to store the buttons for each column
buttons = []

# Loop through each column in the dataset
for col in data.columns:
    # Create a button for the current column
    button = Button(label=f"Activate/Deactivate {col} Plot", button_type="success")
    # Create a JavaScript callback to toggle the visibility of the line plot for the current column
    callback = CustomJS(args=dict(line_plot=plots[col]), code="""
        line_plot.visible = !line_plot.visible;
        """)
    # Assign the callback to the button's js_on_click property
    button.js_on_click(callback)
    # Add the button to the buttons list
    buttons.append(button)

# Create a layout for the buttons and the plot
button_layout = column(*buttons)
layout = row(button_layout, plot)

# Add the layout to the current document
curdoc().add_root(layout)
