#!/usr/bin/python3
'''
Subclasses BluetoothSocket to serve messages "LOW" and "HIGH" based on values received from
client

Copyright Simon D. Levy 2018

MIT License
'''

from pyserver import BluetoothServer
from csv_manager import getTouchInfo


class LightServer(BluetoothServer):

    def __init__(self):

        BluetoothServer.__init__(self)
        
        self.count = 0
        self.touch2out = getTouchInfo()

    def handleTouch(self, s, curr_state):
        try: 
            out = self.touch2out[s]
            lst = list(curr_state)
            lst[int(s)-1]  = out #-1 because s is 1 indexed
            out_str = ''.join(lst)
            self.send(out_str)
        except: 
            out_str = curr_state
        return out_str

        
    def handleReady(self, message): 
    	print()

if __name__ == '__main__':
	server = LightServer()
	# playsound('renegade.mp3')

	server.start()