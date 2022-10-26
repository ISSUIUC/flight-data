#include <iostream>
#include <fstream>
#include <cstring>


using systime_t = uint32_t;
/**
 * @brief Structure for all values collected from the low g sensor
 *
 */


class RocketFSM {
public:
    /**
     * @brief Labels for each FSM state
     */
    enum class FSM_State {
        STATE_INIT,
        STATE_IDLE,
        STATE_LAUNCH_DETECT,
        STATE_BOOST,
        STATE_BURNOUT_DETECT,
        STATE_COAST_PREGNC,
        STATE_COAST_GNC,
        STATE_APOGEE_DETECT,
        STATE_APOGEE,
        STATE_DROGUE_DETECT,
        STATE_DROGUE,
        STATE_MAIN_DETECT,
        STATE_MAIN,
        STATE_LANDED_DETECT,
        STATE_LANDED,
        STATE_ABORT
    };

    virtual void tickFSM() = 0;

    FSM_State getFSMState() const { return rocket_state_; }

protected:
    FSM_State rocket_state_ = FSM_State::STATE_INIT;
};

struct VoltageData {
    float v_battery;
    float v_servo1;
    float v_servo2;
    float v_3_3;
    float v_5;
    float v_9;
    systime_t timestamp;
};

/**
 * @brief Structure for all values collected from the low g sensor
 *
 */
struct LowGData {
    float ax;
    float ay;
    float az;
    float gx;
    float gy;
    float gz;
    float mx;
    float my;
    float mz;
    systime_t timeStamp_lowG;
};

/**
 * @brief Structure for all values collected from the high g sensor
 *
 */
struct HighGData {
    float hg_ax;
    float hg_ay;
    float hg_az;
    systime_t timeStamp_highG;
};

/**
 * @brief Structure for all values collected from the gps
 *
 */
struct GpsData {
    float latitude;
    float longitude;
    float altitude;
    uint32_t siv_count;
    uint32_t fix_type;
    bool posLock;
    systime_t timeStamp_GPS;
};

struct FlapData {
    float extension;
    systime_t timeStamp_flaps;
};

/**
 * @brief Structure for all values collected from the barometer
 *
 */
struct BarometerData {
    float temperature;  // in degC
    float pressure;     // in mbar
    float altitude;     // in meter
    systime_t timeStamp_barometer;
};

/**
 * @brief Structure for all values tracked for state estimation
 *
 */
struct stateData {
    float state_x = 0;
    float state_vx = 0;
    float state_ax = 0;
    float state_apo = 0;

    systime_t timeStamp_state = 0;
};

/**
 * @brief Structure for all values related to rocket state
 *
 */
template <size_t count>
struct rocketStateData {
    RocketFSM::FSM_State rocketStates[count];
    systime_t timeStamp_RS = 0;

    rocketStateData() : rocketStates() {
        for (size_t i = 0; i < count; i++) {
            rocketStates[i] = RocketFSM::FSM_State::STATE_INIT;
        }
    }
};

/**
 * @brief A struct to hold all of the data that could come from any of the
 * sensors
 *
 */
struct sensorDataStruct_t {
    // data for lowGimu
    bool has_lowG_data;
    LowGData lowG_data;

    // data for highGimu accel data (hg_x, hg_y, hg_z)
    bool has_highG_data;
    HighGData highG_data;

    // GPS DATA
    bool has_gps_data;
    GpsData gps_data;

    // Barometer data (temp and pres)
    bool has_barometer_data;
    BarometerData barometer_data;

    // State variables
    bool has_state_data;
    stateData state_data;

    // Rocket State
    bool has_rocketState_data;
    rocketStateData<1> rocketState_data;

    // Flap state
    bool has_flap_data;
    FlapData flap_data;

    // Voltage state
    bool has_voltage_data;
    VoltageData voltage_data;
};

int main(int argc, char ** argv) {
    if(argc != 3){
        std::cout << "usage: inputfile outputfile" << std::endl;
        return 1;
    }

    std::ifstream input{argv[1], std::ios::binary};
    std::ofstream output{argv[2]};

    auto header = "binary logging of sensor_data_t";
    char buff[1024];
    input.read(buff, strlen(header) + 2);
    output
    << "has_lowG_data" << ","
    << "lowG_data.ax" << ","
    << "lowG_data.ay" << ","
    << "lowG_data.az" << ","
    << "lowG_data.gx" << ","
    << "lowG_data.gy" << ","
    << "lowG_data.gz" << ","
    << "lowG_data.mx" << ","
    << "lowG_data.my" << ","
    << "lowG_data.mz" << ","
    << "lowG_data.timestamp" << ",";



    output
    << "has_gps_data" << ","
    << "gps_data.altitude" << ","
    << "gps_data.fix_type" << ","
    << "gps_data.latitude" << ","
    << "gps_data.longitude" << ","
    << "gps_data.posLock" << ","
    << "gps_data.siv_count" << ","
    << "gps_data.timestamp" << ",";

    output
    << "has_barometer_data" << ","
    << "barometer_data.temperature" << ","
    << "barometer_data.altitude" << ","
    << "barometer_data.pressure" << ","
    << "barometer_data.timestamp" << ",";

    output
    << "has_rocketState_data" << ","
    << "rocketState_data.rocketState" << ","
    << "rocketState_data.timestamp" << ",";

    output
    << "has_highG_data" << ","
    << "highG_data.ax" << ","
    << "highG_data.ay" << ","
    << "highG_data.az" << ","
    << "highG_data.timestamp" << ",";

    output
    << "has_flap_data" << ","
    << "flap_data.l1" << ","
    << "flap_data.l2" << ","
    << "flap_data.timestamp" << ",";

    output
    << "has_state_data" << ","
    << "state_data.x" << ","
    << "state_data.vx" << ","
    << "state_data.ax" << ","
    << "state_data.apo" << ","
    << "state_data.timestamp" << ",";

    output
    << "has_voltage_data" << ","
    << "voltage_data.timestamp" << ","
    << "voltage_data.battery_voltage" << "\n";

    while(true){
        sensorDataStruct_t data;
        input.read(reinterpret_cast<char*>(&data), sizeof(data));
        if(!input){
            return 0;
        }

        output
        << data.has_lowG_data << ","
        << data.lowG_data.ax << ","
        << data.lowG_data.ay << ","
        << data.lowG_data.az << ","
        << data.lowG_data.gx << ","
        << data.lowG_data.gy << ","
        << data.lowG_data.gz << ","
        << data.lowG_data.mx << ","
        << data.lowG_data.my << ","
        << data.lowG_data.mz << ","
        << data.lowG_data.timeStamp_lowG << ",";



        output
        << data.has_gps_data << ","
        << data.gps_data.altitude << ","
        << data.gps_data.fix_type << ","
        << data.gps_data.latitude << ","
        << data.gps_data.longitude << ","
        << data.gps_data.posLock << ","
        << data.gps_data.siv_count << ","
        << data.gps_data.timeStamp_GPS << ",";

        output
        << data.has_barometer_data << ","
        << data.barometer_data.temperature << ","
        << data.barometer_data.altitude << ","
        << data.barometer_data.pressure << ","
        << data.barometer_data.timeStamp_barometer << ",";

        output
        << data.has_rocketState_data << ","
        << static_cast<int>(data.rocketState_data.rocketStates[0]) << ","
        << data.rocketState_data.timeStamp_RS << ",";

        output
        << data.has_highG_data << ","
        << data.highG_data.hg_ax << ","
        << data.highG_data.hg_ay << ","
        << data.highG_data.hg_az << ","
        << data.highG_data.timeStamp_highG << ",";

        output
        << data.has_flap_data << ","
        << data.flap_data.extension << ","
        << data.flap_data.timeStamp_flaps << ",";

        output
        << data.has_state_data << ","
        << data.state_data.state_x << ","
        << data.state_data.state_vx << ","
        << data.state_data.state_ax << ","
        << data.state_data.state_apo << ","
        << data.state_data.timeStamp_state << ",";

        output
        << data.has_voltage_data << ","
        << data.voltage_data.timestamp << ","
        << data.voltage_data.v_battery << "\n";
    }
}