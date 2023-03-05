import csv
import json

# Open the JSON file and load its contents into a variable called data
with open('data91.json') as f:
    doc = json.load(f)

# The data variable now contains the contents of the JSON file as a dictionary
# You can access individual values using keys:
#doc = pd.read_csv('/Users/aadityavoruganti/ISS/FlightaViea/flight-data/raw_csv.csv')
#"has_kalman_data": false, "kalman_data": {"kalman_pos_x": 0.0, "kalman_vel_x": 0.0, "kalman_acc_x": 0.0, "kalman_pos_y": 0.0, "kalman_vel_y": 0.0, "kalman_acc_y": 0.0, "kalman_pos_z": 0.0, "kalman_vel_z": 0.0, "kalman_acc_z": 0.0, "kalman_apo": 0.0, "timeStamp_state": 0}, "has_rocketState_data": true, "rocketState_data": {"rocketStates": ["STATE_IDLE", "STATE_INIT", "STATE_IDLE", "STATE_IDLE"], "timestamp": 144

def to_ms(timestamp):
    return timestamp // 100

def find_next_index(idx, timestamp, time_stamp_col, has_data_col):
    while idx < len(time_stamp_col):
        if has_data_col[idx] and to_ms(time_stamp_col[idx]) > timestamp:
            return idx
        idx += 1

    return len(time_stamp_col) - 1

def reformat(output_file, doc, step, start_time, end_time):
    ax = [item['lowG_data']['ax'] for item in doc]
    ay = [item['lowG_data']['ay'] for item in doc]
    az = [item['lowG_data']['az'] for item in doc]
    gx = [item['lowG_data']['gx'] for item in doc]
    gy = [item['lowG_data']['gy'] for item in doc]
    gz = [item['lowG_data']['gz'] for item in doc]
    #mx = [item['lowG_data']['mx'] for item in doc]
    #my = [item['lowG_data']['my'] for item in doc]
    #mz = [item['lowG_data']['mz'] for item in doc]
    latitude = [item['gps_data']['latitude'] for item in doc]
    longitude = [item['gps_data']['longitude'] for item in doc]
    altitude = [item['gps_data']['altitude'] for item in doc]
    satellite_count = [item['gps_data']['siv_count'] for item in doc]
    position_lock = [item['gps_data']['posLock'] for item in doc]
    temperature = [item['barometer_data']['temperature'] for item in doc]
    pressure = [item['barometer_data']['pressure'] for item in doc]
    barometer_altitude = [item['barometer_data']['altitude'] for item in doc]
    extension = [item['flap_data']['extension'] for item in doc]
    has_gps_data = [int(item['has_gps_data']) for item in doc]
    has_lowG_data = [int(item['has_lowG_data']) for item in doc]
    has_baro_data = [int(item['has_barometer_data']) for item in doc]
    #has_fsm_data = [item["has_rocketState_data"] for item in doc]
    has_flap_data = [int(item["has_flap_data"]) for item in doc]
    has_highg_data = [int(item["has_highG_data"]) for item in doc]
    highg_ax = [item["highG_data"]["hg_ax"] for item in doc]
    highg_ay = [item["highG_data"]["hg_ay"] for item in doc]
    highg_az = [item["highG_data"]["hg_az"] for item in doc]
    highg_timestamp = [item["highG_data"]["timeStamp_highG"] for item in doc]
    gps_timestamp = [item["gps_data"]["timeStamp_GPS"] for item in doc]
    lowG_timestamp = [item["lowG_data"]["timeStamp_lowG"] for item in doc]
    baro_timestamp = [item["barometer_data"]["timeStamp_barometer"] for item in doc]
    bno_ax = [item["orientation_data"]["accel"]["ax"] for item in doc]
    bno_ay = [item["orientation_data"]["accel"]["ay"] for item in doc]
    bno_az = [item["orientation_data"]["accel"]["az"] for item in doc]
    bno_gx = [item["orientation_data"]["gyro"]["gx"] for item in doc]
    bno_gy = [item["orientation_data"]["gyro"]["gy"] for item in doc]
    bno_gz = [item["orientation_data"]["gyro"]["gz"] for item in doc]
    bno_mx = [item["orientation_data"]["magnet"]["mx"] for item in doc]
    bno_my = [item["orientation_data"]["magnet"]["my"] for item in doc]
    bno_mz = [item["orientation_data"]["magnet"]["mz"] for item in doc]
    bno_yaw = [item["orientation_data"]["angle"]["yaw"] for item in doc]
    bno_pitch = [item["orientation_data"]["angle"]["pitch"] for item in doc]
    bno_roll = [item["orientation_data"]["angle"]["roll"] for item in doc]
    magnet_mx = [item["magnetometer_data"]["magnetometer"]["mx"] for item in doc]
    magnet_my = [item["magnetometer_data"]["magnetometer"]["my"] for item in doc]
    magnet_mz = [item["magnetometer_data"]["magnetometer"]["mz"] for item in doc]
    gas_temp = [item["gas_data"]["temp"] for item in doc]
    gas_humidity = [item["gas_data"]["humidity"] for item in doc]
    gas_pressure = [item["gas_data"]["pressure"] for item in doc]
    gas_resistance = [item["gas_data"]["resistance"] for item in doc]
    #fsm_timestamp = [item["rocketState_data.timeStamp_RS"] for item in doc]
    flap_timestamp = [item["flap_data"]["timeStamp_flaps"] for item in doc]
    bno_timestamp = [item["orientation_data"]["timeStamp_orientation"] for item in doc]
    magnet_timestamp = [item["magnetometer_data"]["timestamp"] for item in doc]
    gas_timestamp = [item["gas_data"]["timestamp"] for item in doc]
    #state_timestamp = [item["state_data"]["timestamp"] for item in doc]
    #has_state_data = [item["has_state_data"] for item in doc]
    #state_x = [item["state_data.state_x"] for item in doc]
    #state_vx = [item["state_data.state_vx"] for item in doc]
    #state_ax = [item["state_data.state_ax"] for item in doc]
    #state_apo = [item["state_data.state_apo"] for item in doc]
    voltage_battery = [item["voltage_data"]["v_battery"] for item in doc]
    voltage_timestamp = [item["voltage_data"]["timestamp"] for item in doc]
    has_voltage_data = [int(item["has_voltage_data"]) for item in doc]
    has_bno_data = [int(item["has_orientation_data"]) for item in doc]
    has_magnetometer_data = [int(item["has_magnetometer_data"]) for item in doc]
    has_gas_data = [int(item["has_gas_data"])for item in doc]



    with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp_ms", "ax", "ay", "az", "gx", "gy", "gz",
                            "latitude", "longitude", "altitude", "satellite_count", "position_lock",
                            "temperature", "pressure", "barometer_altitude", "highg_ax", "highg_ay", "highg_az",
                            "extension", "voltage_battery","bno_ax","bno_ay","bno_az","bno_gx", "bno_gy", "bno_gz"
                            , "bno_mx", "bno_my","bno_mz", "bno_yaw", "bno_pitch", "bno_roll","magnet_mx",
                            "magnet_my","magnet_mz", "gas_temp", "gas_pressure", "gas_humidity", "gas_resistance"])
            gps_index, lowg_index, baro_index, fsm_index, flap_index, highg_index, voltage_index, state_index,bno_index,magnet_index,gas_index = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            for time in range(start_time, end_time, step):
                gps_index = find_next_index(gps_index, time, gps_timestamp, has_gps_data)
                lowg_index = find_next_index(lowg_index, time, lowG_timestamp, has_lowG_data)
                baro_index = find_next_index(baro_index, time, baro_timestamp, has_baro_data)
                #fsm_index = find_next_index(fsm_index, time, fsm_timestamp, has_fsm_data)
                highg_index = find_next_index(highg_index, time, highg_timestamp, has_highg_data)
                flap_index = find_next_index(flap_index, time, flap_timestamp, has_flap_data)
                #state_index = find_next_index(state_index, time, state_timestamp, has_state_data)
                voltage_index = find_next_index(voltage_index, time, voltage_timestamp, has_voltage_data)
                bno_index = find_next_index(bno_index,time,bno_timestamp,has_bno_data)
                magnet_index = find_next_index(magnet_index,time,magnet_timestamp,has_magnetometer_data)
                gas_index = find_next_index(gas_index,time,gas_timestamp, has_gas_data)


                writer.writerow([time,
                                ax[lowg_index], ay[lowg_index], az[lowg_index],
                                gx[lowg_index], gy[lowg_index], gz[lowg_index],
                                latitude[gps_index], longitude[gps_index], altitude[gps_index] / 1000.0,
                                satellite_count[gps_index], position_lock[gps_index],
                                temperature[baro_index], pressure[baro_index], barometer_altitude[baro_index],
                                highg_ax[highg_index], highg_ay[highg_index], highg_az[highg_index],
                                extension[flap_index], voltage_battery[voltage_index], bno_ax[bno_index],bno_ay[bno_index],
                                bno_az[bno_index], bno_gx[bno_index], bno_gy[bno_index],bno_gz[bno_index],bno_mx[bno_index]
                                ,bno_my[bno_index], bno_mz[bno_index], bno_yaw[bno_index], bno_pitch[bno_index], 
                                bno_roll[bno_index], magnet_mx[magnet_index],magnet_my[magnet_index],magnet_mz[magnet_index],
                                gas_temp[gas_index], gas_pressure[gas_index], gas_humidity[gas_index], gas_resistance[gas_index]])          


reformat("flightcomputer.csv", doc, 10, 0, 29300)