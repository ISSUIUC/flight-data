# flight-data
HAS BEEN MIGRATED TO https://uofi.box.com/s/4tiz5087w0k0o5c8q6ztsot6nda5cbi3 

## Past Flights
[20211030](https://github.com/ISSUIUC/flight-data/tree/master/20211030) -- **Endurance, TARS mk2** <br/>
[20220507](https://github.com/ISSUIUC/flight-data/tree/master/20220507) -- **Intrepid I, TARS mk3** <br/>
[20220623](https://github.com/ISSUIUC/flight-data/tree/master/20220623) -- **Intrepid II, TARS mk3** <br/>
[20221029](https://github.com/ISSUIUC/flight-data/tree/master/20221029) -- **Intrepid III, Test Flight 1, TARS mk3.1** <br/>
[20230305](https://github.com/ISSUIUC/flight-data/tree/master/20230305) -- **Intrepid III, Test Flight 2, TARS mk4** <br/>
[20230507](https://github.com/ISSUIUC/flight-data/tree/master/20230507) -- **Stargazer I, COTS** <br/>
[20230621](https://github.com/ISSUIUC/flight-data/tree/master/20230621) -- **Intrepid III, Competition Launch, TARS mk4** <br/>


## Flight Data Decommissioning
##### DURING ROCKET RECOVERY
- Take pictures of **ALL** components immediately after being recovered. Verify status of all igniters & E-matches **AFTER** verifying that energetics are disabled.
- Ensure all altimeters are present and functioning

##### AFTER RETURNING TO CAMPUS
- Download all SD card data to local machine (If applicable)
- Download all COTS altimeter data to local machine
	- Plug in altimeters to device with AltOS
	- Connect the 2 **SWITCH** ports with a jumper.
	- Connect a compatible battery to the altimeter
	- After successful beep sequence, open AltOS.
	- Press `Save Flight Data`
	- Select the appropriate altimeter
	- Then download everything.
	- Press `Export Data`
	- Export all `.eeprom` files to `.csv` 
- Retrieve all photos from post-recovery.
- Create a directory with the format `yyyymmdd`
- Save **ALL** SD card data and COTS Altimeter data to new directory
- Create a subdirectory named `photos`
- Upload all post-recovery photos to the `photos` subdirectory
- Upload the entire `yyyymmdd` directory to https://github.com/ISSUIUC/flight-data/tree/master on a new branch
- Edit **this file** to add a link to the directory and the name of the rocket from the launch to the `Past Flights` section

## File meanings: 
 * Data
   * `flight_computer` - Data retrieved from the rocket. (SRAD) <br />
   * `ground_station` - Data transmited from the rocket and logged by the ground station (SRAD) <br />
   * `telemetrum` - Data retrieved from telemetrum flight recordings. (Not data logged by Telemetrum transmissions) (COTS) <br />
   * `stratologger` - Data retrieved from the Stratologger flight recordings. (COTS) <br />
 * Code
   * `parse_data.cpp` - Parse data from a `.dat` to a `.csv` file. 
   * `reformat_data.cpp` - Organize data to simplify data headers and reduce clutter. 
