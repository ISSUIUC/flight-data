import numpy as np
import pandas as pd

from bokeh.layouts import layout
from bokeh.io import curdoc,output_notebook, show
from bokeh.layouts import column, row
from bokeh.models import RangeTool, BoxAnnotation, Toggle, Select, ColumnDataSource, Range1d
from bokeh.plotting import figure, show, output_file
from bokeh.models.widgets import Div



logo = Div(text="<img src='https://drive.google.com/uc?id=1rlfAW6tNZNo0lvKCJSioGHeYONmyNKGU'>", width = 100, height = 75, align = 'start')
flame = Div(text="<img src='https://drive.google.com/uc?id=1b_c2ZBvTqpKswnBGrxzjdmo0wWuRw7Lf'>",width = 200, height = 75, align = 'start')

# updates plot when dropdown item is selected
def update_plot(attr,old,new):
    choice = data_select.value
    p = figure(height=300, width=800, tools="xpan", toolbar_location=None, x_axis_location="below", 
    background_fill_color="#efefef", x_range=(0, len(timestamp)-1), y_range = (0,int(1.5 * max(data[choice]))))

    p.xaxis.axis_label = "Time Elapsed (ms)"
    p.yaxis.axis_label = choice

    p.line(x = [i for i in range(len(timestamp))], y = data[choice])
    p.add_layout(state_1_box)
    p.add_layout(state_2_box)
    p.add_layout(state_3_box)

    curdoc().roots[0].children[2] = p


# loads data into dataframe using pandas
data = pd.read_csv("FlightView/data.csv")


timestamp = data["timestamp"]
state = data["rocket_state"]

# stores start/end of states
st = 1
st_memory = []
choice = 'altitude'

for i in range(len(timestamp)):
    if state[i] > st:
        st_memory.append(i)
        st = state[i]


choices = {}

for i in data:
    choices[i] = 1

# creates data dropdown
data_select = Select(value=choice, title='Series', options=sorted(choices.keys()), height = 50, width = 300)

p = figure(height=300, width=800, tools="xpan", toolbar_location=None, x_axis_location="below", 
background_fill_color="#efefef", x_range=(0, len(timestamp)-1), y_range = (0,int(1.5 * max(data[choice]))))

p.line(x = [i for i in range(len(timestamp))], y = data[choice])

p.xaxis.axis_label = 'Time Elapsed (ms)'
p.yaxis.axis_label = 'Altitude'

data_select.on_change('value', update_plot)

# state boundaries
state_1_box = BoxAnnotation(left=0, right=st_memory[0], fill_color='#fa7e11', fill_alpha=0.1)
state_2_box = BoxAnnotation(left=st_memory[0], right=st_memory[1], fill_color='#0047ab', fill_alpha=0.1)
state_3_box = BoxAnnotation(left=st_memory[1], fill_color='#700038', fill_alpha=0.1)

p.add_layout(state_1_box)
p.add_layout(state_2_box)
p.add_layout(state_3_box)


# button to toggle state boundaries
toggle1 = Toggle(label="State Boxes", button_type="success", active=True)
toggle1.js_link('active', state_1_box, 'visible')
toggle1.js_link('active', state_2_box, 'visible')
toggle1.js_link('active', state_3_box, 'visible')

controls = column(data_select)

curdoc().add_root(column(row(logo,flame),controls,p))
curdoc().title = "FlightView"