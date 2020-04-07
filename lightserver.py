#!/usr/bin/python3
'''
Subclasses BluetoothSocket to serve messages "LOW" and "HIGH" based on values received from
client

Copyright Simon D. Levy 2018

MIT License
'''

from pyserver import BluetoothServer
from csv_manager import getTouchInfo

import sys

BUTTON_COLOR_DURATION = 2


class LightServer(BluetoothServer):

    def __init__(self):

        BluetoothServer.__init__(self)
        
        self.count = 0
        self.touch2out = getTouchInfo()

    # Assuming s is index of color being changed
    def handleTouch(self, s, curr_state, current_time, input_times):
        try: 
            out = self.touch2out[s]
            lst = list(curr_state)
            lst[int(s)-1]  = out #-1 because s is 1 indexed
            out_str = ''.join(lst)

            input_times[int(s)-1] = current_time + BUTTON_COLOR_DURATION

            self.send(out_str)
        except: 
            out_str = curr_state
        return out_str, input_times

        
    def handleReady(self, message): 
    	print()

if __name__ == '__main__':
    if len(sys.argv)!= 3:
        print("\nPlease call the program using:")
        print("\t python lightserver.py audio_file.mp3 timing_file.csv\n")
        exit()

    audio_file_input = sys.argv[1]
    csv_file_input = sys.argv[2]

    server = LightServer()

    server.start(audio_file_input, csv_file_input)
    # server.start()

