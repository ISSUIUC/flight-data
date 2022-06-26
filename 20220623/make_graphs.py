import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("flight_computer.csv")
df = df[223500:]

# sort data based on struct
df_lowG_data = df[df['has_lowG_data'] > 0]
df_highG_data = df[df['has_highG_data'] > 0]
df_barometer_data = df[df['has_barometer_data'] > 0]
df_state_data = df[df['has_state_data'] > 0]

# plot settings
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "monospace"

def plot_lowG_data():
    
    # intialize plotting variables
    timestamp = df_lowG_data["lowG_data.timestamp"].values
    timestamp = (timestamp - min(timestamp))/100000
    fig = plt.figure(dpi=200)
    
    #----------------------------------------------------------------------------------------------#
    
    # plot acceleration
    plt.plot(timestamp, df_lowG_data["lowG_data.ax"].values, label="lowG_data.ax")
    plt.plot(timestamp, df_lowG_data["lowG_data.ay"].values, label="lowG_data.ay")
    plt.plot(timestamp, df_lowG_data["lowG_data.az"].values, label="lowG_data.az")
    
    # format and save plot
    plt.xlabel("Time (s)"); plt.ylabel("Acceleration (G)")
    plt.legend(); plt.grid()
    plt.savefig("plots/lowG_data_acceleration.png")
    fig.clear()
    
    #----------------------------------------------------------------------------------------------#
    
    # plot gyroscope
    plt.plot(timestamp, df_lowG_data["lowG_data.gx"].values, label="lowG_data.gx")
    plt.plot(timestamp, df_lowG_data["lowG_data.gy"].values, label="lowG_data.gy")
    plt.plot(timestamp, df_lowG_data["lowG_data.gz"].values, label="lowG_data.gz")
    
    # format and save plot
    plt.xlabel("Time (s)"); plt.ylabel("Gyroscope (deg/s)")
    plt.legend(); plt.grid()
    plt.savefig("plots/lowG_data_gyroscope.png")
    fig.clear()
    
    #----------------------------------------------------------------------------------------------#
    
    # plot magnetometer
    plt.plot(timestamp, df_lowG_data["lowG_data.mx"].values, label="lowG_data.mx")
    plt.plot(timestamp, df_lowG_data["lowG_data.my"].values, label="lowG_data.my")
    plt.plot(timestamp, df_lowG_data["lowG_data.mz"].values, label="lowG_data.mz")
    
    # format and save plot
    plt.xlabel("Time (s)"); plt.ylabel("Magnetometer (Gauss)")
    plt.legend(); plt.grid()
    plt.savefig("plots/lowG_data_magnetometer.png")
    fig.clear()
    
    
def plot_highG_data():
    
    # intialize plotting variables
    timestamp = df_highG_data["highG_data.timestamp"].values
    timestamp = (timestamp - min(timestamp))/100000
    fig = plt.figure(dpi=200)
    
    # plot acceleration
    plt.plot(timestamp, df_highG_data["highG_data.ax"].values, label="highG_data.ax")
    plt.plot(timestamp, df_highG_data["highG_data.ay"].values, label="highG_data.ay")
    plt.plot(timestamp, df_highG_data["highG_data.az"].values, label="highG_data.az")
    
    # format and save plot
    plt.xlabel("Time (s)"); plt.ylabel("Acceleration (G)")
    plt.legend(); plt.grid()
    plt.savefig("plots/highG_data_acceleration.png")
    fig.clear()
    
    
def plot_barometer_data():
    
    # intialize plotting variables
    timestamp = df_barometer_data["barometer_data.timestamp"].values
    timestamp = (timestamp - min(timestamp))/100000
    fig = plt.figure(dpi=200)
    
    #----------------------------------------------------------------------------------------------#
    
    # settings for dual axis plot
    fig_2axes, ax_pressure = plt.subplots(dpi=200)
    ax_temperature = ax_pressure.twinx()
    
    # plot raw barometer data
    ax_pressure.plot(timestamp, df_barometer_data["barometer_data.pressure"].values, 
                     label="pressure", color="tab:blue", zorder=10)
    ax_temperature.plot(timestamp, df_barometer_data["barometer_data.temperature"].values, 
                        label="temperature", color="tab:orange", zorder=10)
    
    # format and save plot
    ax_pressure.set_xlabel("Time (s)")
    ax_pressure.set_ylabel("Pressure (mbar)"); ax_temperature.set_ylabel("Temperature (deg C)")
    ax_pressure.grid(True)
    plt.savefig("plots/barometer_data_raw.png")
    fig_2axes.clear()
    
    #----------------------------------------------------------------------------------------------#
    
    # plot barometric altitude 
    plt.plot(timestamp, df_barometer_data["barometer_data.altitude"].values)
    
    # format and save plot
    plt.xlabel("Time (s)"); plt.ylabel("Barometric Altitude (m)")
    plt.grid()
    plt.savefig("plots/barometer_data_altitude.png")
    fig.clear()
    
    
def plot_state_data():
    
    # intialize plotting variables
    timestamp_state = df_state_data["state_data.timestamp"].values/100000
    timestamp_barometer = df_barometer_data["barometer_data.timestamp"].values/100000
    fig = plt.figure(dpi=200)
    
    # plot altitudes
    plt.plot(timestamp_state, df_state_data["state_data.x"].values, label="State")
    plt.plot(timestamp_barometer, df_barometer_data["barometer_data.altitude"].values, label="Barometric")
    
    # format and save plot
    plt.xlabel("Time (s)"); plt.ylabel("Altitude (m)")
    plt.legend(); plt.grid()
    plt.savefig("plots/state_comparison.png")
    fig.clear()
    
    
if __name__ == '__main__':
    plot_lowG_data()
    plot_barometer_data()
    plot_highG_data()
    plot_state_data()