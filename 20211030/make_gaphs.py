import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./trimmed.csv")

timestamp_seconds = df.timestamp/1000

# check the csv for what columns there are

# the data in trimmed.csv is from right before launch to right after landing
# if you only care about data on ascent or descent use these functions


def trim_ascent_only(array):
    return array[500:3000]


def trim_descent_only(array):
    return array[2800:20000]


timestamps_ascent = trim_descent_only(timestamp_seconds)
baro_altitude_ascent = trim_descent_only(df.barometer_altitude)


# altitude is altitude from gps, it has no data from during the ascent for anti-icbm reasons
# barometer_altitude is altitude as a function of pressure
# It can be used for altitude during the ascent but it is scaled a little wrong
# the y direction points down
# so gy = -20 means that the rocket is accelerating upwards at 20 gs
# ax, ay, az are acceleration
# gx, gy, gz are angular velocity around the x,y,z axies
# mx, my, mz are angular acceleration
# l1_extension and l2_extension are what the flap extensions would be if the flaps are turned on
# flaps are only turned on when rocket_state = 5
# ask Nicholas Phillips if you have questions on the data


# you may have to scale some columns so they fit on the plot with each other
plt.plot(timestamp_seconds, df.ay*100)
plt.plot(timestamp_seconds, df.barometer_altitude)
plt.plot(timestamp_seconds, df.altitude)
plt.show()


