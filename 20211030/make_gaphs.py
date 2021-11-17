import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./trimmed.csv")

timestamp_seconds = df.timestamp/1000

# data
# timestamp: milliseconds since power on

# lowgimu data:
#   ax: acceleration in the x direction (lateral, gs)
#   ay: acceleration in the y direction (vertical, down is positive, gs)
#   az: acceleration in the z direction (lateral, gs)
#   gx: angular velocity on the x axis
#   gy: angular velocity on the y axis (roll)
#   gz: angular velocity on the z axis
#   mx: magnetometer(compass) direction on the x axis
#   my: magnetometer(compass) direction on the y axis (roll)
#   mz: magnetometer(compass) direction on the z axis

# gps data:
#   latitude: gps latitude (degrees)
#   longitude: gps longitude (degrees)
#   altitude: gps altitude (meters, no data on ascent)
#   satellite_count: number of connected satellites (integer, more means bettter data)
#   position_lock: weather the gps has a lock (boolean, 1 = has connection)

# barometer data:
#   temperature: Celsius
#   pressure: millibar
#   barometer_altitude: altitude calculated from pressure (meters, a little higher than the real number)

# rocket state data:
#   rocket_state:
#       0: Startup
#       1: Waiting for launch
#       2: Launch transition
#       3: Boost phase
#       4: Boost-coast transition
#       5: Coast, flaps move
#       6: Coast-apogee transition (unused)
#       7: Post apogee

# flap data: flaps only physically move when rocket_state = 5
#   l1_extension: requested flap length (meters, real flap length is clamped to about 2cm)
#   l2_extension: requested flap length (meters, real flap length is clamped to about 2cm)

# ask Nicholas Phillips if you have questions on the data

# the data in trimmed.csv is from right before launch to right after landing
# if you only care about data on ascent or descent use these functions


def trim_ascent_only(array):
    return array[500:3000]


def trim_descent_only(array):
    return array[2800:20000]


# ascent only example
timestamps_ascent = trim_ascent_only(timestamp_seconds)
baro_altitude_ascent = trim_ascent_only(df.barometer_altitude)
plt.plot(timestamps_ascent, baro_altitude_ascent)
plt.show()


# descent only example
timestamps_descent = trim_descent_only(timestamp_seconds)
baro_altitude_descent = trim_descent_only(df.barometer_altitude)
plt.plot(timestamps_descent, baro_altitude_descent)
plt.show()

# you may have to scale some columns so they fit on the plot with each other
# full data example
plt.plot(timestamp_seconds, df.ay*100)
plt.plot(timestamp_seconds, df.barometer_altitude)
plt.plot(timestamp_seconds, df.altitude)
plt.show()


