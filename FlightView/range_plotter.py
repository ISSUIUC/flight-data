from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, Range1d, LinearAxis
from bokeh.plotting import figure, show
from bokeh.palettes import Dark2_5 as palette
import itertools
import pandas as pd

def range_plotter(csv, list_of_keys):
    df = pd.read_csv(csv)
    time_data = df['timestamp_ms']
    data_arrays = []

    source = ColumnDataSource(df)

    p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(time_data[1500], time_data[2500]))
    
    p.extra_y_ranges = {}
    for i, key in enumerate(list_of_keys):
        p.extra_y_ranges[key + '_axis'] = Range1d(start=min(df[key]) - 0.1*(max(df[key]) - min(df[key])), end=max(df[key]) + 0.1*(max(df[key]) - min(df[key])))
        p.line('timestamp_ms', key, source=source, color=palette[i], y_range_name=(key+'_axis'))
        p.add_layout(LinearAxis(y_range_name=(key+'_axis'), axis_label=key), 'left')
    p.yaxis.visible = True
    
    select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")
    
    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2
    
    for i, key in enumerate(list_of_keys):
        select.extra_y_ranges[key + '_axis'] = Range1d(start=min(df[key]), end=max(df[key]))
        select.line('timestamp_ms', key, source=source, color=palette[i], y_range_name=(key+'_axis'))
        select.add_layout(LinearAxis(y_range_name=(key+'_axis'), axis_label=key), 'left')
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool
    show(column(p, select))

range_plotter('20221029/flight_computer.csv', ['barometer_altitude', 'az'])
df = pd.read_csv('20221029/flight_computer.csv')
print(max(df['az']))
