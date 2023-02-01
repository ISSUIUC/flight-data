import itertools
import numpy as np
import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure, show, curdoc
from bokeh.palettes import Dark2_5 as palette
from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn,
                          Legend, RangeTool, Range1d, LinearAxis, Button,
                          CheckboxGroup, CustomJS)

# Load the flight data from the CSV file
mpg = pd.read_csv("https://raw.githubusercontent.com/ISSUIUC/flight-data/master/20221029/flight_computer.csv")

#Create a ColumnDataSource from the flight data
source = ColumnDataSource(mpg)

timearr = mpg['timestamp_ms'].div(10000)

axs = sorted(mpg["ax"].unique())
ays = sorted(mpg["ay"].unique())
azs = sorted(mpg["az"].unique())
time = sorted(mpg["timestamp_ms"].unique())


columns = [
    TableColumn(field="ax", title="axs",
                editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0000")),
    TableColumn(field="ay", title="ays",
                editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0000")),
    TableColumn(field="az", title="azs",
                editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0000")),
    TableColumn(field="timestamp_ms", title="timestamp_ms",
                editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0000")),    
]

data_table = DataTable(source=source, columns=columns, editable=True, width=800,
                       index_position=-1, index_header="row index", index_width=60)

p = figure(width=800, height=300, tools="pan,wheel_zoom,xbox_select,reset", active_drag="xbox_select")
p.circle(x="index", y="ax", fill_color="#396285", size=8, alpha=0.5, source=source)
ay = p.circle(x="index", y="ay", fill_color="#CE603D", size=8, alpha=0.5, source=source)

ax = p.circle(x="index", y="ax", fill_color="#396285", size=8, alpha=0.5, source=source)
ay = p.circle(x="index", y="ay", fill_color="#CE603D", size=8, alpha=0.5, source=source)

tooltips = [
    ("ax", "@ax"),
    ("ay", "@ay"),
    ("az", "@az"),
    ("timearr","@time")
]

cty_hover_tool = HoverTool(renderers=[ax], tooltips=tooltips + [("time", "@time")])
hwy_hover_tool = HoverTool(renderers=[ay], tooltips=tooltips + [("ax", "@ax")])
p.add_tools(cty_hover_tool, hwy_hover_tool)


# Create a ColumnDataSource for the ax, ay, and az
source_relevent = ColumnDataSource(data={
    'a': np.arange(len(mpg['ax'])),
    'x': mpg['ax'],
    'y': mpg['ay'],
    'z': mpg['az']
})

# Create a figure with three line plots: ax, ay, and az
f = figure(width=800, height=400)
f.line('a', 'y', source=source_relevent, legend_label='ax')
f.line('a', 'z', source=source_relevent, legend_label='ay', line_color='green')
f.line('a', 'x', source=source_relevent, legend_label='az', line_color='red')

# Create a legend and add the 'legend_hide' feature
legend = Legend(items=[
    ('ax', [f.renderers[0]]),
    ('ay', [f.renderers[1]]),
    ('az', [f.renderers[2]])
], location='top_left')
legend.click_policy = 'hide'
f.add_layout(legend, 'left')

#make altitude and mx plot
time_data = mpg['timestamp_ms']
alt_data = mpg['barometer_altitude']
mx_data = mpg['mx']
my_data = mpg['my']
source = ColumnDataSource(mpg)

g = figure(height=300, width=1600, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(time_data[1500], time_data[2500]))

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=1600, y_range=g.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=g.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2


select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool


#define a range plotter that will take a list of keys and a csv and create plots
def range_plotter(list_of_keys):
    
    g.extra_y_ranges = {}
    for i, key in enumerate(list_of_keys):
        g.extra_y_ranges[key + '_axis'] = Range1d(start=min(mpg[key]) - 0.1*(max(mpg[key]) - min(mpg[key])), end=max(mpg[key]) + 0.1*(max(mpg[key]) - min(mpg[key])))
        g.line('timestamp_ms', key, source=source, color=palette[i], y_range_name=(key+'_axis'))
        g.add_layout(LinearAxis(y_range_name=(key+'_axis'), axis_label=key), 'left')
    g.yaxis.visible = True
    
    for i, key in enumerate(list_of_keys):
        select.extra_y_ranges[key + '_axis'] = Range1d(start=min(mpg[key]), end=max(mpg[key]))
        select.line('timestamp_ms', key, source=source, color=palette[i], y_range_name=(key+'_axis'))
        select.add_layout(LinearAxis(y_range_name=(key+'_axis'), axis_label=key), 'left')
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool

LABELS = ['timestamp_ms', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz',
       'latitude', 'longitude', 'altitude', 'satellite_count', 'position_lock',
       'temperature', 'pressure', 'barometer_altitude', 'highg_ax', 'highg_ay',
       'highg_az', 'rocket_state0', 'rocket_state1', 'rocket_state2',
       'rocket_state3', 'flap_extension', 'state_est_x', 'state_est_vx',
       'state_est_ax', 'state_est_apo', 'battery_voltage']

checkbox_group = CheckboxGroup(labels=LABELS)
def update(attr, old, new):
    # Get the list of active keys
    active_keys = [checkbox_group.labels[i] for i in 
                        checkbox_group.active]
    
    range_plotter(active_keys)
checkbox_group.on_change('active', update)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(data_table, row(p,f), column(g,select,checkbox_group)))