//
// Created by 16182 on 10/31/2021.
//

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

    auto rocket_state = doc.GetColumn<size_t>("rocketState_data.rocketState");
    auto l1_extension = doc.GetColumn<double>("flap_data.l1");
    auto l2_extension = doc.GetColumn<double>("flap_data.l2");

    auto has_gps_data = doc.GetColumn<size_t>("has_gps_data");
    auto has_lowG_data = doc.GetColumn<size_t>("has_lowG_data");
    auto has_baro_data = doc.GetColumn<size_t>("has_barometer_data");
    auto has_fsm_data = doc.GetColumn<size_t>("has_rocketState_data");
    auto has_flap_data = doc.GetColumn<size_t>("has_flap_data");

    auto has_highg_data = doc.GetColumn<size_t>("had_highg_data");
    auto highg_ax = doc.GetColumn<double>("highg_data.ax");
    auto highg_ay = doc.GetColumn<double>("highg_data.ay");
    auto highg_az = doc.GetColumn<double>("highg_data.az");
    auto highg_timestamp = doc.GetColumn<size_t>("highg_data.timestamp");

    auto gps_timestamp = doc.GetColumn<size_t>("gps_data.timestamp");
    auto lowG_timestamp = doc.GetColumn<size_t>("lowG_data.timestamp");
    auto baro_timestamp = doc.GetColumn<size_t>("barometer_data.timestamp");
    auto fsm_timestamp = doc.GetColumn<size_t>("rocketState_data.timestamp");
    auto flap_timestamp = doc.GetColumn<size_t>("flap_data.timestamp");
    auto voltage_timestamp = doc.GetColumn<size_t>("voltage_data.timestamp");
    auto state_timestamp = doc.GetColumn<size_t>("state_data.timestamp");

    auto has_state_data = doc.GetColumn<size_t>("has_state_data");
    auto state_x = doc.GetColumn<double>("state_data.x");
    auto state_vx = doc.GetColumn<double>("state_data.vx");
    auto state_ax = doc.GetColumn<double>("state_data.ax");
    auto state_apo = doc.GetColumn<double>("state_data.apo");

    auto has_voltage_data = doc.GetColumn<size_t>("has_voltage_data");
    auto voltage_battery = doc.GetColumn<double>("voltage_data.battery_voltage");

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

    file << "rocket_state" << ",";
    file << "l1_extension" << ",";
    file << "l2_extension" << ",";

    file << "state_est_x" << ",";
    file << "state_est_vx" << ",";
    file << "state_est_ax" << ",";
    file << "state_est_apo" << ",";

    file << "battery_voltage" << "\n";

    for(size_t time = start_time; time < end_time; time += step){
        gps_index = find_next_index(gps_index, time, gps_timestamp, has_gps_data);
        lowg_index = find_next_index(lowg_index, time, lowG_timestamp, has_lowG_data);
        baro_index = find_next_index(baro_index, time, baro_timestamp, has_baro_data);
        fsm_index = find_next_index(fsm_index, time, fsm_timestamp, has_fsm_data);
        highg_index = find_next_index(highg_index, time, highg_timestamp, has_highg_data);
        flap_index = find_next_index(flap_index, time, flap_timestamp, has_flap_data);
        state_index = find_next_index(state_index, time, state_timestamp, has_state_data);
        voltage_index = find_next_index(voltage_index, time, voltage_timestamp, has_voltage_data);

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

        file << rocket_state[fsm_index] << ",";
        file << l1_extension[flap_index] << ",";
        file << l2_extension[flap_index] << ",";

        file << state_x[state_index] << ",";
        file << state_vx[state_index] << ",";
        file << state_ax[state_index] << ",";
        file << state_apo[state_index] << ",";

        file << voltage_battery[voltage_index] << "\n";
    }
}

int main(){
    rapidcsv::Document doc("irec.csv");
    reformat(std::ofstream("trimmed_irec.csv"), doc, 10, 4935750, 4937700);
}