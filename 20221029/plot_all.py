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
import matplotlib.pyplot as plt
import numpy as np


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
plt.style.use("dark_background")
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

def plot_mach_data():

    # Calculating atmospheric temperature using the US Standard Atmospheric Model 
    # and the Kalman filter estimated altitude
    altitude_asl = df["state_est_x"] + 219 # in m, 219m is the elevation of launch site
    ambient_T = 15.04 - 0.00649*altitude_asl + 273.15 # K

    
    Mach = np.zeros(3500) # Calculating Mach with US Standard Temp 
    Mach_bad = np.zeros(3500) # Calculating Mach number with Barometer Temp
    gamma = 1.4
    R = 287 # J/(kg*K)
    for i in range(3500):
        Mach[i] = df["state_est_vx"][i]/np.sqrt(gamma*R*ambient_T[i])
        Mach_bad[i] = df["state_est_vx"][i]/np.sqrt(gamma*R*(df["temperature"][i] + 273.15))
    
    # Finding the time at which Mach number first hits 1
    supersonic_start = tstamp[np.where(np.isclose(Mach, 1.0, rtol=1e-1))[0][0]]
    print('Approximate time when rocket hits sound barrier =', supersonic_start, 'ms')

    # intialize plotting variables
    fig = plt.figure(dpi=200)

    # Plotting Ambient Temperature
    plt.plot(tstamp, ambient_T - 273.15, label="Ambient Temperature (C)")
    plt.xlabel("Time (ms)")
    plt.ylabel("Temperature")
    plt.legend()
    plt.grid()
    plt.title("US Standard Atmospheric Model Temperature")
    plt.savefig("plots/standard_temp_model.png")
    fig.clear()

    # Plotting Mach Number
    plt.plot(tstamp[0:3500], Mach, label="Mach with US Standard Temp")
    plt.plot(tstamp[0:3500], Mach_bad, label="Mach with Barometer Temp")
    plt.xlabel("Time (ms)")
    plt.ylabel("Mach Number")
    plt.legend()
    plt.grid()
    plt.title("Mach Number")
    plt.savefig("plots/mach_number.png")
    fig.clear()

    # Plotting Mach Number and Barometer Pressure near Transonic Flow
    fig_2axes, ax_pressure = plt.subplots(dpi=200)
    ax_mach = ax_pressure.twinx()
    
    # plot raw barometer data
    ax_pressure.plot(tstamp[500:1000], df["pressure"][500:1000], 
                     label="pressure", color="tab:blue", zorder=10)
    ax_mach.plot(tstamp[500:1000], Mach[500:1000], 
                        label="mach number", color="tab:orange", zorder=10)
    
    # format and save plot
    ax_pressure.set_xlabel("Time (ms)")
    ax_pressure.set_ylabel("Pressure (mbar)", color="tab:blue"); ax_mach.set_ylabel("Mach Number", color="tab:orange")
    ax_pressure.grid(True)
    plt.title("Baro Pressure and Mach around Transonic Flow")
    plt.savefig("plots/pressure_and_mach.png")
    fig_2axes.clear()

def plot_fsm_with_altitude_data():
    fig_2axes, fsmState = plt.subplots(dpi=200)
    altitude = fsmState.twinx()
    # plot fsm states 

    #indexes for apogee
    #startIndex, endIndex = 2750, 3500

    #indexes for whole flight
    #startIndex, endIndex = 0, -1

    #indexes for landed
    startIndex, endIndex = 4000, -1

    fsmState.plot(tstamp[startIndex:endIndex], df["rocket_state2"][startIndex:endIndex], label = "History Buffer 6")
    fsmState.plot(tstamp[startIndex:endIndex], df["rocket_state1"][startIndex:endIndex], label = "History Buffer 50")
    fsmState.plot(tstamp[startIndex:endIndex], df["rocket_state3"][startIndex:endIndex], label = "Kalman")
    altitude.plot(tstamp[startIndex:endIndex], df["barometer_altitude"][startIndex:endIndex], label = "Altitude", color="tab:orange")
    
    # format and save plot
    fsmState.set_xlabel("Time (ms)"); 
    fsmState.set_ylabel("FSM State")
    altitude.set_ylabel("Altitude (m)")
    fsmState.legend()
    altitude.legend()
    plt.title("FSM States Near Landing")
    plt.savefig("plots/fsm_states_and_altitude_near_landing.png")
    fig_2axes.clear()

def plot_fsm_with_acceleration_data():
    fig_2axes, fsmState = plt.subplots(dpi=200)
    altitude = fsmState.twinx()
    # plot fsm states 
    startIndex, endIndex = 3050, 3300
    fsmState.plot(tstamp[startIndex:endIndex], df["rocket_state2"][startIndex:endIndex], label = "History Buffer 6")
    fsmState.plot(tstamp[startIndex:endIndex], df["rocket_state1"][startIndex:endIndex], label = "History Buffer 50")
    fsmState.plot(tstamp[startIndex:endIndex], df["rocket_state3"][startIndex:endIndex], label = "Kalman")
    altitude.plot(tstamp[startIndex:endIndex], df["highg_az"][startIndex:endIndex], label = "Acceleration", color="tab:orange")
    
    # format and save plot
    fsmState.set_xlabel("Time (ms)"); 
    fsmState.set_ylabel("FSM State")
    altitude.set_ylabel("Acceleration (gs)")
    fsmState.legend()
    altitude.legend()
    plt.title("FSM States Near Separation")
    plt.savefig("plots/fsm_states_and_acceleration.png")
    fig_2axes.clear()


if __name__ == '__main__':
    # plot_lowG_data()
    # plot_barometer_data()
    # plot_highG_data()
    # plot_state_data()
    #plot_mach_data()
    plot_fsm_with_altitude_data()
    #plot_fsm_with_acceleration_data()
    #print(tstamp)