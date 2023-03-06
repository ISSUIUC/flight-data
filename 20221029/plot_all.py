"""
Illinois Space Society

Data Plotting Script

 _______       _____   _____ 
|__   __|/\   |  __ \ / ____|
   | |  /  \  | |__) | (___  
   | | / /\ \ |  _  / \___ \ 
   | |/ ____ \| | \ \ ____) |
   |_/_/    \_\_|  \_\_____/ 

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("flight_computer.csv")
tstamp = df["timestamp_ms"] - df["timestamp_ms"][0]
fsm_names = ["Init",
            "Idle",
            "Launch Detect",
            "Boost",
            "Burnout Detect",
            "Coast Pre GNC",
            "Coast GNC",
            "Apogee Detect",
            "Apogee",
            "Drogue Detect",
            "Drogue Descent",
            "Main Detect",
            "Main Descent",
            "Landed Detect",
            "Landed"]


plt.rcParams["font.family"] = "monospace"
# plt.style.use("dark_background")
# plt.style.use("Solarized_Light2")

def plot_lowG_data():
    
    # intialize plotting variables
    fig = plt.figure(dpi=200)
    
    #----------------------------------------------------------------------------------------------#
    
    # plot acceleration
    # plt.plot(timestamp, df_lowG_data["lowG_data.ax"].values, label="lowG_data.ax")
    # plt.plot(timestamp, df_lowG_data["lowG_data.ay"].values, label="lowG_data.ay")
    # plt.plot(timestamp, df_lowG_data["lowG_data.az"].values, label="lowG_data.az")
    
    # # format and save plot
    # plt.xlabel("Time (s)"); plt.ylabel("Acceleration (G)")
    # plt.legend(); plt.grid()
    # plt.savefig("plots/lowG_data_acceleration.png")
    # fig.clear()
    
    # #----------------------------------------------------------------------------------------------#
    tstamp_pre_apo = tstamp[250:3350]
    df_pre_apo = df[250:3350]

    # plot gyroscope
    plt.plot(tstamp_pre_apo, df_pre_apo["gx"], label="gx")
    plt.plot(tstamp_pre_apo, df_pre_apo["gy"], label="gy")
    # plt.plot(tstamp_pre_apo, df_pre_apo["gz"], label="gz")
    
    # format and save plot
    plt.xlabel("Time (ms)"); plt.ylabel("Rotational Velocity (deg/s)")
    plt.title("Gyroscope Data (Until Apogee) - LSM9DS1")
    plt.legend(); plt.grid()
    plt.savefig("plots/lowG_data_gyroscope.png")
    fig.clear()
    
    #----------------------------------------------------------------------------------------------#
    
    # plot magnetometer
    plt.plot(tstamp_pre_apo, df_pre_apo["mx"], label="mx")
    plt.plot(tstamp_pre_apo, df_pre_apo["my"], label="my")
    plt.plot(tstamp_pre_apo, df_pre_apo["mz"], label="mz")
    
    # format and save plot
    plt.xlabel("Time (ms)"); plt.ylabel("Magnetic Flux Density (Gauss)")
    plt.legend(); plt.grid()
    plt.title("Magnetometer Data (Until Apogee) - LSM9DS1")
    plt.savefig("plots/lowG_data_magnetometer.png")
    fig.clear()
    
    
def plot_highG_data():
    
    # intialize plotting variables

    fig = plt.figure(dpi=200)
    
    # plot acceleration
    # plt.plot(tstamp, df["highg_ax"], label="ax")
    # plt.plot(tstamp, df["highg_ay"], label="ay")
    plt.plot(tstamp[0:3500], df["highg_az"][0:3500], label="az")
    print(max(df["highg_az"]))
    
    # format and save plot
    plt.xlabel("Time (ms)"); plt.ylabel("Acceleration (G)")
    plt.title("Accelerometer Data (Until Apogee) - KX134")
    plt.legend()
    # plt.grid()
    plt.savefig("plots/highG_data_acceleration_az_only_until_apogee.png")
    fig.clear()
    
    
def plot_barometer_data():
    
    # intialize plotting variables
    # timestamp = df_barometer_data["barometer_data.timestamp"].values
    # timestamp = (timestamp - min(timestamp))/100000
    fig = plt.figure(dpi=200)
    
    #----------------------------------------------------------------------------------------------#
    
    # settings for dual axis plot
    fig_2axes, ax_pressure = plt.subplots(dpi=200)
    ax_temperature = ax_pressure.twinx()
    
    # plot raw barometer data
    ax_pressure.plot(tstamp, df["pressure"], 
                     label="pressure", color="tab:blue", zorder=10)
    ax_temperature.plot(tstamp, df["temperature"], 
                        label="temperature", color="tab:orange", zorder=10)
    
    # format and save plot
    ax_pressure.set_xlabel("Time (ms)")
    ax_pressure.set_ylabel("Pressure (mbar)"); ax_temperature.set_ylabel("Temperature (deg C)")
    ax_pressure.grid(True)
    plt.title("Barometer Data - MS5611")
    plt.savefig("plots/barometer_data_raw.png")
    fig_2axes.clear()
    
    #----------------------------------------------------------------------------------------------#
    
    # plot barometric altitude 
    plt.plot(tstamp, df["barometer_altitude"])
    
    # format and save plot
    plt.xlabel("Time (ms)"); plt.ylabel("Altitude (m)")
    plt.grid()
    plt.title("Barometric Altitude - MS5611")
    plt.savefig("plots/barometer_data_altitude.png")
    fig.clear()
    
    
def plot_state_data():
    
    # intialize plotting variables
    # timestamp_state = df_state_data["state_data.timestamp"].values/100000
    # timestamp_barometer = df_barometer_data["barometer_data.timestamp"].values/100000
    fig = plt.figure(dpi=200)
    
    # plot altitudes
    plt.plot(tstamp, df["barometer_altitude"].values, label="Barometric")
    plt.plot(tstamp, df["state_est_apo"].values, label="State")
    
    
    # format and save plot
    plt.xlabel("Time (ms)"); plt.ylabel("Altitude (m)")
    plt.legend(); plt.grid()
    plt.title("Barometric Atitude vs Predicted Apogee")
    plt.savefig("plots/state_comparison_apo.png")
    fig.clear()

    #-----------------------------------------------------------------------------------------------------#

    plt.plot(tstamp[0:3500], df["state_est_vx"][0:3500], label="KF Velocity")
    plt.xlabel("Time (ms)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid()
    plt.title("State Estimation Velocity (Until Apogee)")
    plt.savefig("plots/state_vx.png")

def plot_flap_baro_coupling():
    tstamp_pre_apo = tstamp[250:3350]
    df_pre_apo = df[250:3350]
    plt.plot(tstamp_pre_apo, df_pre_apo["pressure"].values, label="Barometric Pressure")
    plt.title("Time vs Barometric Pressure")
    plt.xlabel("Time (ms)")
    plt.ylabel("Pressure (mbar)")
    plt.axvline(3100, color = 'tab:green' , label="Start of Motor Burn")
    plt.axvline(6800, color = 'tab:red' ,label="End of Motor Burn")
    plt.axvline(7800, color = 'orange' ,label="Flap Extension Start")
    plt.axvline(8800, color = 'blue' ,label="Flap Retraction Start ")
    plt.axvline(9450, color = 'purple' ,label="Flap Retraction End")
    plt.axvline(11800, color = 'orange')
    plt.axvline(31050, color = 'pink', label="Apogee")
    plt.legend()
    plt.savefig("plots/GNC_Baro_investigation.png")
    plt.show()
    
if __name__ == '__main__':
    # plot_lowG_data()
    # plot_barometer_data()
    # plot_highG_data()
    # plot_state_data()
    plot_flap_baro_coupling()