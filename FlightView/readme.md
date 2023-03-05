# FlightView Version 0.1

## Steps to run the FlightView by parsing raw data.

1. First run data_parser.py in the following manner python3 data_parser.py data-header.hpp [raw data file]. For example in this repo launch91.launch is converted to launch91.json

2. Second the parser outputs a raw data file, this file now needs to be passed as input into parsejsondata.py on the 5th line the line should be changed to look like this with 

open('[parsed file output]') as f:. 

A csv file named flightcomputer.csv is outputed

3. There are 2 options the static HTML site flightview or a real-time running flightview that runs a dash app. The latter has a maximum and minimum table as well for each value. Both apps can be run like a normal python file and will. If the static app is used a html file is outputed and can be used on a browser. If using the static app then open http://127.0.0.1:8050/ on the browser. (Dash App may take a few seconds)
