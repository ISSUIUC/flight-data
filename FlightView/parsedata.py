import math
import csv
import pandas as pd

doc = pd.read_csv('flightcomputer.csv')

def to_ms(timestamp):
    return timestamp // 100

def find_next_index(idx, timestamp, time_stamp_col, has_data_col):
    while idx < len(time_stamp_col):
        if has_data_col[idx] and to_ms(time_stamp_col[idx]) > timestamp:
            return idx
        idx += 1

    return len(time_stamp_col) - 1

def reformat(output_file, doc, step, start_time, end_time):
    ax = doc["lowG_data.ax"]
    ay = doc["lowG_data.ay"]
    az = doc["lowG_data.az"]
    gx = doc["lowG_data.gx"]
    gy = doc["lowG_data.gy"]
    gz = doc["lowG_data.gz"]
    mx = doc["lowG_data.mx"]
    my = doc["lowG_data.my"]
    mz = doc["lowG_data.mz"]
    latitude = doc["gps_data.latitude"]
    longitude = doc["gps_data.longitude"]
    altitude = doc["gps_data.altitude"]
    satellite_count = doc["gps_data.siv_count"]
    position_lock = doc["gps_data.posLock"]
    temperature = doc["barometer_data.temperature"]
    pressure = doc["barometer_data.pressure"]
    barometer_altitude = doc["barometer_data.altitude"]
    FSM_timer = doc["rocketState_data.rocketState0"]
    FSM_hist_50 = doc["rocketState_data.rocketState1"]
    FSM_hist_6 = doc["rocketState_data.rocketState2"]
    FSM_GNC = doc["rocketState_data.rocketState3"]
    extension = doc["flap_data.extension"]
    has_gps_data = doc["has_gps_data"]
    has_lowG_data = doc["has_lowG_data"]
    has_baro_data = doc["has_barometer_data"]
    has_fsm_data = doc["has_rocketState_data"]
    has_flap_data = doc["has_flap_data"]
    has_highg_data = doc["has_highG_data"]
    highg_ax = doc["highG_data.ax"]
    highg_ay = doc["highG_data.ay"]
    highg_az = doc["highG_data.az"]
    highg_timestamp = doc["highG_data.timeStamp_highG"]
    gps_timestamp = doc["gps_data.timeStamp_GPS"]
    lowG_timestamp = doc["lowG_data.timeStamp_lowG"]
    baro_timestamp = doc["barometer_data.timeStamp_barometer"]
    fsm_timestamp = doc["rocketState_data.timeStamp_RS"]
    flap_timestamp = doc["flap_data.timeStamp_flaps"]
    state_timestamp = doc["state_data.timeStamp_state"]
    has_state_data = doc["has_state_data"]
    state_x = doc["state_data.state_x"]
    state_vx = doc["state_data.state_vx"]
    state_ax = doc["state_data.state_ax"]
    state_apo = doc["state_data.state_apo"]
    voltage_battery = doc["voltage_data.v_battery"]
    has_voltage_data = doc["has_voltage_data"]


    with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp_ms", "ax", "ay", "az", "gx", "gy", "gz", "mx", "my", "mz",
                            "latitude", "longitude", "altitude", "satellite_count", "position_lock",
                            "temperature", "pressure", "barometer_altitude", "highg_ax", "highg_ay", "highg_az",
                            "FSM_timer", "FSM_hist_50", "FSM_hist_6", "FSM_GNC", "extension", "state_est_x",	
                            "state_est_vx",	"state_est_ax",	"state_est_apo","voltage_battery"])
            gps_index, lowg_index, baro_index, fsm_index, flap_index, highg_index, voltage_index, state_index = 0, 0, 0, 0, 0, 0, 0, 0
            for time in range(start_time, end_time, step):
                gps_index = find_next_index(gps_index, time, gps_timestamp, has_gps_data)
                lowg_index = find_next_index(lowg_index, time, lowG_timestamp, has_lowG_data)
                baro_index = find_next_index(baro_index, time, baro_timestamp, has_baro_data)
                fsm_index = find_next_index(fsm_index, time, fsm_timestamp, has_fsm_data)
                highg_index = find_next_index(highg_index, time, highg_timestamp, has_highg_data)
                flap_index = find_next_index(flap_index, time, flap_timestamp, has_flap_data)
                state_index = find_next_index(state_index, time, state_timestamp, has_state_data)
                voltage_index = find_next_index(voltage_index, time, baro_timestamp, has_voltage_data)

                writer.writerow([time,
                                ax[lowg_index], ay[lowg_index], az[lowg_index],
                                gx[lowg_index], gy[lowg_index], gz[lowg_index],
                                mx[lowg_index], my[lowg_index], mz[lowg_index],
                                latitude[gps_index], longitude[gps_index], altitude[gps_index] / 1000.0,
                                satellite_count[gps_index], position_lock[gps_index],
                                temperature[baro_index], pressure[baro_index], barometer_altitude[baro_index],
                                highg_ax[highg_index], highg_ay[highg_index], highg_az[highg_index],
                                FSM_timer[fsm_index], FSM_hist_50[fsm_index], FSM_hist_6[fsm_index], FSM_GNC[fsm_index],
                                extension[flap_index], state_x[state_index], state_vx[state_index],
                                state_ax[state_index], state_apo[state_index],voltage_battery[voltage_index]])


reformat("output.csv", doc, 10, 1945435, 2135322)
