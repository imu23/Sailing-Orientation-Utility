Processor:

process.py is the main processing script. It uses the individual sensor process scripts to perform those calculations separately. It has a reference to the database and a process_bmp object as well as the functions to smooth data. 

The main function of the process.py script accesses the rawEx table in the database. It will take a set amount of rows (from the given index, passed in as a parameter, to the end of the table) and perform processing on each individual datum in each row. A list of each type of data is made from this processed data, and this list is then smoothed according to an exponential smoothing algorithm. The date and time are simply chosen to be the last values in the list (i.e., the most recent values). The processed values are then returned in a new list (also saved for reference to be used by the error smoothing algorithm), which is used in the main.py script.

The error smoothing is a very simple algorithm and could easily be improved on. The error smoothing/filtering method in general could be improved by comparing data types. For example, if the speed, accelerometer, gyroscope return 0 or change, this is an indication that the device is not in motion, therefore if the heading is changing, it is likely false information. 

Process_<sensor>:

Each of the sensors has its own processing script that takes the raw data from the registers and processes it into a usable value. This conversion is usually described in the data sheets for the sensors.

The temperature/pressure sensor has its own process_bmp.py in addition to a process_temp.py and process_press.py. This is because the sensor itself needs to be calibrated and include a lot of bit manipulation to get each real data value. This sensor requires a sleep time between accessing the two different values. This may or may not be handled properly. Run the process_bmp.py OR run both the process_temp.py and process_press.py, but not both. The process_bmp.py has procTemp and procPress functions to find the processed values from raw data.

The temperature/pressure sensor data can also be used to calculate altitude and the pressure at sea level. These are done in process_extra_bmp.py (although they have not been tested). The method to do these were included in the example sensor scripts available through Adafruit.

The magnetometer uses the accelerometer in order to find an accurate heading, since the compass needs to be flat. Using the accelerometer data will reduce the error from the magnetometer being tilted. 

The magnetometer also required being calibrated (only once). A small, simple script was used to find the min and max x,y, and z values. If the magnetometer seems to be inaccurate, try calibrating the magnetometer by running this script while rotating the sensor completely around every axis. The calibrated values can then be entered into the proccess_compass.py script.

The accelerometer also uses the gyroscope in order to reduce the amount of gravitational acceleration being calculated into the data.

