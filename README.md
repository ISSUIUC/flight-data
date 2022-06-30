# flight-data
Flight data collected from past launches

Files shall be uploaded as a `.csv` and contain the raw data unless specified otherwise. Each launch shall be separated with a directory with the format: `yyyymmdd`.

## File meanings: <br />

 * Data
   * `flight_computer` - Data retrieved from the rocket. (SRAD) <br />
   * `ground_station` - Data transmited from the rocket and logged by the ground station (SRAD) <br />
   * `telemetrum` - Data retrieved from telemetrum flight recordings. (Not data logged by Telemetrum transmissions) (COTS) <br />
   * `stratologger` - Data retrieved from the Stratologger flight recordings. (COTS) <br />
 * Code
   * `parse_data.cpp` - Parse data from a `.dat` to a `.csv` file. 
   * `reformat_data.cpp` - Organize data to simplify data headers and reduce clutter.
