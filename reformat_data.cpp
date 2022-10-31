//
// Tool to clean up log file and fit all data to a single time series
//
//   _______       _____   _____ 
//  |__   __|/\   |  __ \ / ____|
//     | |  /  \  | |__) | (___  
//     | | / /\ \ |  _  / \___ \ 
//     | |/ ____ \| | \ \ ____) |
//     |_/_/    \_\_|  \_\_____/ 

#include "rapidcsv.h"
#include <fstream>
#include <numeric>
int64_t to_ms(int64_t timestamp){
    return timestamp / 100;
}

size_t find_next_index(size_t idx, size_t timestamp, const auto & time_stamp_col, const auto & has_data_col){
    while(idx < time_stamp_col.size()){
        if(has_data_col[idx] && to_ms(time_stamp_col[idx]) > timestamp){
            return idx;
        }
        idx ++;
    }

    return time_stamp_col.size() - 1;
}

void reformat(std::ofstream file, const rapidcsv::Document & doc, size_t step, size_t start_time, size_t end_time){
    auto ax = doc.GetColumn<double>("lowG_data.ax");
    auto ay = doc.GetColumn<double>("lowG_data.ay");
    auto az = doc.GetColumn<double>("lowG_data.az");
    auto gx = doc.GetColumn<double>("lowG_data.gx");
    auto gy = doc.GetColumn<double>("lowG_data.gy");
    auto gz = doc.GetColumn<double>("lowG_data.gz");
    auto mx = doc.GetColumn<double>("lowG_data.mx");
    auto my = doc.GetColumn<double>("lowG_data.my");
    auto mz = doc.GetColumn<double>("lowG_data.mz");
    auto latitude = doc.GetColumn<double>("gps_data.latitude");
    auto longitude = doc.GetColumn<double>("gps_data.longitude");
    auto altitude = doc.GetColumn<double>("gps_data.altitude");
    auto satellite_count = doc.GetColumn<size_t>("gps_data.siv_count");
    auto position_lock = doc.GetColumn<size_t>("gps_data.posLock");

    auto temperature = doc.GetColumn<double>("barometer_data.temperature");
    auto pressure = doc.GetColumn<double>("barometer_data.pressure");
    auto barometer_altitude = doc.GetColumn<double>("barometer_data.altitude");

    auto FSM_timer = doc.GetColumn<size_t>("rocketState_data.rocketState0");
    auto FSM_hist_50 = doc.GetColumn<size_t>("rocketState_data.rocketState1");
    auto FSM_hist_6 = doc.GetColumn<size_t>("rocketState_data.rocketState2");
    auto FSM_GNC = doc.GetColumn<size_t>("rocketState_data.rocketState3");
    auto extension = doc.GetColumn<double>("flap_data.extension");

    auto has_gps_data = doc.GetColumn<size_t>("has_gps_data");
    auto has_lowG_data = doc.GetColumn<size_t>("has_lowG_data");
    auto has_baro_data = doc.GetColumn<size_t>("has_barometer_data");
    auto has_fsm_data = doc.GetColumn<size_t>("has_rocketState_data");
    auto has_flap_data = doc.GetColumn<size_t>("has_flap_data");

    auto has_highg_data = doc.GetColumn<size_t>("has_highG_data");
    auto highg_ax = doc.GetColumn<double>("highG_data.ax");
    auto highg_ay = doc.GetColumn<double>("highG_data.ay");
    auto highg_az = doc.GetColumn<double>("highG_data.az");
    auto highg_timestamp = doc.GetColumn<size_t>("highG_data.timeStamp_highG");

    auto gps_timestamp = doc.GetColumn<size_t>("gps_data.timeStamp_GPS");
    auto lowG_timestamp = doc.GetColumn<size_t>("lowG_data.timeStamp_lowG");
    auto baro_timestamp = doc.GetColumn<size_t>("barometer_data.timeStamp_barometer");
    auto fsm_timestamp = doc.GetColumn<size_t>("rocketState_data.timeStamp_RS");
    auto flap_timestamp = doc.GetColumn<size_t>("flap_data.timeStamp_flaps");
    // auto voltage_timestamp = doc.GetColumn<size_t>("voltage_data.timestamp");
    auto state_timestamp = doc.GetColumn<size_t>("state_data.timeStamp_state");

    auto has_state_data = doc.GetColumn<size_t>("has_state_data");
    auto state_x = doc.GetColumn<double>("state_data.state_x");
    auto state_vx = doc.GetColumn<double>("state_data.state_vx");
    auto state_ax = doc.GetColumn<double>("state_data.state_ax");
    auto state_apo = doc.GetColumn<double>("state_data.state_apo");

    // auto has_voltage_data = doc.GetColumn<size_t>("has_voltage_data");
    // auto voltage_battery = doc.GetColumn<double>("voltage_data.battery_voltage");

    size_t gps_index{}, lowg_index{}, baro_index{}, fsm_index{}, flap_index{}, highg_index{},
    voltage_index{}, state_index{};

    file << "timestamp_ms" << ",";
    file << "ax" << ",";
    file << "ay" << ",";
    file << "az" << ",";
    file << "gx" << ",";
    file << "gy" << ",";
    file << "gz" << ",";
    file << "mx" << ",";
    file << "my" << ",";
    file << "mz" << ",";

    file << "latitude" << ",";
    file << "longitude" << ",";
    file << "altitude" << ",";
    file << "satellite_count" << ",";
    file << "position_lock" << ",";

    file << "temperature" << ",";
    file << "pressure" << ",";
    file << "barometer_altitude" << ",";

    file << "highg_ax" << ",";
    file << "highg_ay" << ",";
    file << "highg_az" << ",";

    file << "FSM_timer" << ",";
    file << "FSM_hist_50" << ",";
    file << "FSM_hist_6" << ",";
    file << "FSM_GNC" << ",";

    file << "flap_extension" << ",";
    // file << "l2_extension" << ",";

    file << "state_est_x" << ",";
    file << "state_est_vx" << ",";
    file << "state_est_ax" << ",";
    file << "state_est_apo" << "\n";

    // file << "battery_voltage" << "\n";

    for(size_t time = start_time; time < end_time; time += step){
        gps_index = find_next_index(gps_index, time, gps_timestamp, has_gps_data);
        lowg_index = find_next_index(lowg_index, time, lowG_timestamp, has_lowG_data);
        baro_index = find_next_index(baro_index, time, baro_timestamp, has_baro_data);
        fsm_index = find_next_index(fsm_index, time, fsm_timestamp, has_fsm_data);
        highg_index = find_next_index(highg_index, time, highg_timestamp, has_highg_data);
        flap_index = find_next_index(flap_index, time, flap_timestamp, has_flap_data);
        state_index = find_next_index(state_index, time, state_timestamp, has_state_data);
        // voltage_index = find_next_index(voltage_index, time, voltage_timestamp, has_voltage_data);

        file << time << ",";
        file << ax[lowg_index] << ",";
        file << ay[lowg_index] << ",";
        file << az[lowg_index] << ",";
        file << gx[lowg_index] << ",";
        file << gy[lowg_index] << ",";
        file << gz[lowg_index] << ",";
        file << mx[lowg_index] << ",";
        file << my[lowg_index] << ",";
        file << mz[lowg_index] << ",";

        file << latitude[gps_index] << ",";
        file << longitude[gps_index] << ",";
        file << altitude[gps_index] / 1000.0 << ",";
        file << satellite_count[gps_index] << ",";
        file << position_lock[gps_index] << ",";

        file << temperature[baro_index] << ",";
        file << pressure[baro_index] << ",";
        file << barometer_altitude[baro_index] << ",";

        file << highg_ax[highg_index] << ",";
        file << highg_ay[highg_index] << ",";
        file << highg_az[highg_index] << ",";

        file << FSM_timer[fsm_index] << ",";
        file << FSM_hist_50[fsm_index] << ",";
        file << FSM_hist_6[fsm_index] << ",";
        file << FSM_GNC[fsm_index] << ",";

        file << extension[flap_index] << ",";

        file << state_x[state_index] << ",";
        file << state_vx[state_index] << ",";
        file << state_ax[state_index] << ",";
        file << state_apo[state_index] << "\n";

        // file << voltage_battery[voltage_index] << "\n";
    }
}

int main(){
    rapidcsv::Document doc("data3.csv");
    reformat(std::ofstream("flight_computer.csv"), doc, 10, 1945435, 2135322);
}