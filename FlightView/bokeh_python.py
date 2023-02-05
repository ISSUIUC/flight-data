import pandas as pd
import ctypes
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.palettes import Spectral6, Greys9
from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                          NumberEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, TableColumn,
                          Legend, Label, RangeTool, Range1d, LinearAxis, Button,
                          CheckboxGroup, CustomJS, TapTool)
from math import floor

"""Start of Table/Filtering Tool"""

# Load the flight data from the CSV file
df = pd.read_csv("https://raw.githubusercontent.com/ISSUIUC/flight-data/master/20221029/flight_computer.csv")

#Create a ColumnDataSource from the flight data
source = ColumnDataSource(df)

timearr = df['timestamp_ms'].div(10000)

axs = sorted(df["highg_ax"].unique())
ays = sorted(df["highg_ay"].unique())
azs = sorted(df["highg_az"].unique())
time = sorted(df["timestamp_ms"].unique())

columns = [
    TableColumn(field="highg_ax", title="Acceleration in X-Direction",
                editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0000")),
    TableColumn(field="highg_ay", title="Acceleration in Y-Direction",
                editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0000")),
    TableColumn(field="highg_az", title="Acceleration in Z-Direction",
                editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0000")),
    TableColumn(field="timestamp_ms", title="Time (ms)",
                editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0000")),
]


data_table = DataTable(source=source, columns=columns, editable=True, width=1600,
                       index_position=-1, index_header="row index", index_width=60, background='lightgrey')

p = figure(height=500, width=1600, tools="pan,wheel_zoom,xbox_select,reset", active_drag="xbox_select",
           x_axis_label="Time (ms)", y_axis_label="Acceleration", border_fill_color = Greys9[1])
# p.title.text_font_size = "50px"
# p.title_location = "above"

ax = p.circle(x="index", y="highg_ax", fill_color= Spectral6[1], size=4, alpha=0.5, source=source)
ay = p.circle(x="index", y="highg_ay", fill_color= Spectral6[3], size=4, alpha=0.5, source=source)
az = p.circle(x="index", y="highg_az", fill_color= Spectral6[5], size=4, alpha=0.5, source=source)

# taptool = p.select(type=TapTool)
# taptool.behavior = 'inspect' # 'inspect', 'select'


tooltips = [
    ("ax", "@ax"),
    ("ay", "@ay"),
    ("az", "@az"),
    ("timearr","@time")
]

cty_hover_tool = HoverTool(renderers=[ax], tooltips=tooltips + [("time", "@time")])
hwy_hover_tool = HoverTool(renderers=[ay], tooltips=tooltips + [("ax", "@ax")])


# Create a figure with three line plots: ax, ay, and az
# p = figure(width=800, height=300, tools="pan,wheel_zoom,xbox_select,reset", active_drag="xbox_select")
# p.line(x="index", y="ax", source=source, legend_label='ax')
# p.line(x="index", y="ay", source=source, legend_label='ay', line_color='green')
# p.line(x="index", y="az", source=source, legend_label='az', line_color='red')


# Create a legend and add the 'legend_hide' feature
legend = Legend(items=[
    ('ax', [p.renderers[0]]),
    ('ay', [p.renderers[1]]),
    ('az', [p.renderers[2]])
], location='top_left')
legend.click_policy = 'hide'
p.add_layout(legend, 'left')

"""Start of Range Tool"""

#make altitude and mx plot
time_data = df['timestamp_ms']
alt_data = df['barometer_altitude']
mx_data = df['mx']
my_data = df['my']

g = figure(height=300, width=1600, tools="poly_select,pan,wheel_zoom,xbox_select,reset,xpan",
           x_axis_type="datetime", x_axis_location="above", x_range=(time_data[1500], time_data[2500]),
           border_fill_color = Greys9[1])

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=1600, y_range=g.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, border_fill_color = Greys9[1])


#define a range plotter that will take a list of keys and a csv and create plots
def range_plotter(list_of_keys):

    g.extra_y_ranges = {}
    for i, key in enumerate(list_of_keys):
        g.extra_y_ranges[key + '_axis'] = Range1d(start=min(df[key]) - 0.1*(max(df[key]) - min(df[key])), end=max(df[key]) + 0.1*(max(df[key]) - min(df[key])))
        g.line('timestamp_ms', key, source=source, color=palette[i], y_range_name=(key+'_axis'))
        g.add_layout(LinearAxis(y_range_name=(key+'_axis'), axis_label=key), 'left')
    g.yaxis.visible = True

    range_tool = RangeTool(x_range=g.x_range)

    
    for i, key in enumerate(list_of_keys):
        select.extra_y_ranges[key + '_axis'] = Range1d(start=min(df[key]), end=max(df[key]))
        select.line('timestamp_ms', key, source=source, color=palette[i], y_range_name=(key+'_axis'))
        select.add_layout(LinearAxis(y_range_name=(key+'_axis'), axis_label=key), 'left')
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2
    select.toolbar.active_multi = range_tool

LABELS = ['timestamp_ms', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz',
       'latitude', 'longitude', 'altitude', 'satellite_count', 'position_lock',
       'temperature', 'pressure', 'barometer_altitude', 'highg_ax', 'highg_ay',
       'highg_az', 'rocket_state0', 'rocket_state1', 'rocket_state2',
       'rocket_state3', 'flap_extension', 'state_est_x', 'state_est_vx',
       'state_est_ax', 'state_est_apo', 'battery_voltage']

checkbox_group = CheckboxGroup(labels=LABELS, background='lightgrey', width=500)
def update():
    # Get the list of active keys
    active_keys = [checkbox_group.labels[i] for i in 
                        checkbox_group.active]
    range_plotter(active_keys)

# Define the callback to update the visibility of the line
# callback = CustomJS(args=dict(line=line, checkbox=checkbox), code="""""
# if (checkbox.active.includes(0)) {
#     line.visible = false;
# } else {
#     line.visible = true;
# }
# """)

button = Button(label="Update Plots", width=400, height=50)
button.on_event('button_click', update)

logo = figure(x_range=(0,2), y_range=(0,2), tools="", toolbar_location=None, width=1800, height=130, outline_line_alpha = 0,
              border_fill_color = Greys9[1], background_fill_color= Greys9[1])
logo.axis.visible = False
logo.grid.visible = False
logo.image_url(url=['https://lh4.googleusercontent.com/VaLm1JUtRriKE55QAkVyJSjB4JhgtnTYdCqpvnKJGScMdyaxfuJe_wHAohcZuXdK4xL7GXoGcRfAmQ0lYu58h0tBoYJRKdRVZTZZ18oORhSfl16uvQyfrO0F7lM6M84xDw=w1280']
               , x=1.6, y=2, w=0.17, h=2)
logo.image_url(url=['https://lh5.googleusercontent.com/BAIaKZpiQZDAcFD9ssJd766MHhxfp7jQtWIdBcgJcEjgsTeedDpn3GwmZ_WQ1gTLswt8CRCNl__yQ6MMgrYkciZFkTQGsdk3oq34LR7TKzpp8TNLfMOc-0BZ24FGJ4T9EQ=w1280']
               , x=0, y=2, w=0.5, h=2)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(logo,column(data_table,p),column(g,select, row(checkbox_group, button)), background=Greys9[1]))
curdoc().theme = 'dark_minimal'