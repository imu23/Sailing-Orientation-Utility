The driving program is main.py (can be run by typing “python main.py”) it imports all sensor libraries. These libraries allow the main script to poll a particular sensor to access raw data. To understand the raw data the main script imports process.py. This file performs processor functions on each type of sensor data collected. 

Different threads execute individual sensor polls, collected data is placed in a common database. When five new elements are inserted into the rawEx table, the processor is invoked.

The display runs on its own thread automatically refreshing itself. When the processor is invoked, it will update a display instance variable that is an array of strings to output. Before outputting the display calls a data format function that will convert the given data into desired unit.

At the top of the file certain pins are primed as button inputs. Events are created for each pin tied to a button set to detect high input (if the pin reads logic HIGH then the button is pressed). Each event has a callback function associated with the pin. One is a callback that toggles a save variable, the second is one that toggles a scrolling variable. Both variables are instance variables of the eDisplay object. The save determines whether or not output should also be stored in the “saving” table. The scrolling variable determines if the screen alternates between sets of data displayed or continually displays the same set.


