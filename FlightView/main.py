import numpy as np
import pandas as pd

from bokeh.layouts import layout
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import RangeTool, BoxAnnotation, Toggle, Select
from bokeh.plotting import figure, show

# updates plot when dropdown item is selected
def update_plot(attr,old,new):
    print(data_select.value)
    choice = data_select.value
    p = figure(height=300, width=800, tools="xpan", toolbar_location=None, x_axis_location="below", 
    background_fill_color="#efefef", x_range=(0, len(timestamp)-1), y_range = (0,int(1.5 * max(data[choice]))))

    p.xaxis.axis_label = "Time Elapsed (ms)"
    p.yaxis.axis_label = choice

    p.line(x = [i for i in range(len(timestamp))], y = data[choice])
    p.add_layout(state_1_box)
    p.add_layout(state_2_box)
    p.add_layout(state_3_box)

    curdoc().roots[0].children[0] = p



data = pd.read_csv("FlightView/flight_computer_trimmed.csv")


timestamp = data["timestamp_ms"]
state = data["rocket_state"]

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

data_select = Select(value=choice, title='Series', options=sorted(choices.keys()), height = 50, width = 800)

p = figure(height=300, width=800, tools="xpan", toolbar_location=None, x_axis_location="below", 
background_fill_color="#efefef", x_range=(0, len(timestamp)-1), y_range = (0,int(1.5 * max(data[choice]))))

p.line(x = [i for i in range(len(timestamp))], y = data[choice])

p.xaxis.axis_label = 'Time Elapsed (ms)'
p.yaxis.axis_label = 'Altitude'

data_select.on_change('value', update_plot)

state_1_box = BoxAnnotation(left=0, right=st_memory[0], fill_color='#fa7e11', fill_alpha=0.1)
state_2_box = BoxAnnotation(left=st_memory[0], right=st_memory[1], fill_color='#0047ab', fill_alpha=0.1)
state_3_box = BoxAnnotation(left=st_memory[1], fill_color='#700038', fill_alpha=0.1)

p.add_layout(state_1_box)
p.add_layout(state_2_box)
p.add_layout(state_3_box)

toggle1 = Toggle(label="State Boxes", button_type="success", active=True)
toggle1.js_link('active', state_1_box, 'visible')
toggle1.js_link('active', state_2_box, 'visible')
toggle1.js_link('active', state_3_box, 'visible')

show(layout(data_select,p, [toggle1]))

controls = column(data_select)

curdoc().add_root(row(p, controls))
curdoc().title = "FlightView"