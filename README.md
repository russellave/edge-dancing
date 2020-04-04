# edge-dancing

## Android App and Python Server
To run the Android app, I cloned this project: https://github.com/simondlevy/AndroidBluetoothClient

In that project, I changed/added 3 java files in app/src/main/java/. Add/replace the java files in this repo to that directory. I also modified app/src/main/res/layout/activity_communications.xml. Replace that xml file with the xml file in this repo. 

To run the python script, download both lightserver.py and pyserver.py  

## Protocol for Bluetooth
Messages sent end with "."

For the controlling the light colors, there will be a string the length of the number of blocks there are in the app. Each character of the string will represent what color the string will be. The colors will be defined in "color_map.csv" and will be sent to the application at bluetooth initialization. 

### Light Example
Example color map is the following 
Red-->a
Blue-->b
Green-->c

If we have 5 blocks that we want to set to red, red, blue, blue, green respectively, the string sent from the server to the app is "aabbc".





