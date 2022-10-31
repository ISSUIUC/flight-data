"""
Illinois Space Society

Launch Data Formatting Script
"""

import pandas as pd
import matplotlib as plt

filename = "data3.csv"
all_data = pd.read_csv(filename)[100801::]

high_g = all_data[["highG_data.timeStamp_highG", "has_highG_data", "highG_data.ax", "highG_data.ay", "highG_data.az"]]
low_g = all_data[["lowG_data.timeStamp_lowG", "has_lowG_data", "lowG_data.ax", "lowG_data.ay", 
                "lowG_data.az", "lowG_data.gx", "lowG_data.gy", "lowG_data.gz", 
                "lowG_data.mx", "lowG_data.my", "lowG_data.mz"]]
barometer = all_data[["barometer_data.timeStamp_barometer","has_barometer_data", "barometer_data.temperature", "barometer_data.altitude", "barometer_data.pressure"]]
gps = all_data[["gps_data.timeStamp_GPS","has_gps_data", "gps_data.altitude", "gps_data.latitude", "gps_data.longitude", "gps_data.siv_count"]]
fsm = all_data[["rocketState_data.timeStamp_RS", "has_rocketState_data","rocketState_data.rocketState0", "rocketState_data.rocketState1", "rocketState_data.rocketState2", "rocketState_data.rocketState3"]]
gnc = all_data[["state_data.timeStamp_state","has_state_data","state_data.state_x","state_data.state_vx","state_data.state_ax","state_data.state_apo"]]


high_g = high_g[high_g["has_highG_data"] == 1]
low_g = low_g[low_g["has_lowG_data"] == 1]
barometer = barometer[barometer["has_barometer_data"] == 1]
gps = gps[gps["has_gps_data"] == 1]
fsm = fsm[fsm["has_rocketState_data"] == 1]
gnc = gnc[gnc["has_state_data"] == 1]

high_g.to_csv("tars_highg_imu.csv", index=False)
low_g.to_csv("tars_lowg_imu.csv", index=False)
barometer.to_csv("tars_barometer.csv", index=False)
gps.to_csv("tars_gps.csv", index=False)
fsm.to_csv("tars_fsm.csv", index=False)
gnc.to_csv("tars_gnc.csv", index=False)


