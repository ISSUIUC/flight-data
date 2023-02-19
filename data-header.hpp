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

/**
 * @brief Structure for values relevant to active control flaps
 *
 */
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
    // float state_q0 = 0;

    systime_t timeStamp_state = 0;
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

/**
 * @brief Structure for all values related to rocket state
 *
 */
template <size_t count>
struct rocketStateData {
    FSM_State rocketStates[count];
    systime_t timeStamp_RS = 0;

    rocketStateData() : rocketStates() {
        for (size_t i = 0; i < count; i++) {
            rocketStates[i] = FSM_State::STATE_INIT;
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
    rocketStateData<4> rocketState_data;

    // Flap state
    bool has_flap_data;
    FlapData flap_data;

    // Voltage state
    bool has_voltage_data;
    VoltageData voltage_data;
};