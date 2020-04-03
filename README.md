# edge-dancing

## Android App and Python Server
To run the Android app, I cloned this project: https://github.com/simondlevy/AndroidBluetoothClient

In that project, I changed/added 3 java files in app/src/main/java/. Add/replace the java files in this repo to that directory. I also modified app/src/main/res/layout/activity_communications.xml. Replace that xml file with the xml file in this repo. 

To run the python script, download both lightserver.py and pyserver.py  

## Protocol for Bluetooth
Message ends with "."

To control the timing of the messages for song synchronization, app must first send the message ",." to the server, and the server will reply for which lights to turn on. 

The message for one light to turn on will have the following format (rgb values mast have 3 numbers each): 
"<light index 1>:<rvalue 1><gvalue 1><bvalue 1>"

Example: Turn light 3 red-->"3:255000000"

For multiple lights to turn on, each entry will be separated by an underscore. 

Example: Turn light 3 red and light 4 blue-->"3:255000000_4:000000255"
