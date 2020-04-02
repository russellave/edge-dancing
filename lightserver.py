#!/usr/bin/python3
'''
Subclasses BluetoothSocket to serve messages "LOW" and "HIGH" based on values received from
client

Copyright Simon D. Levy 2018

MIT License
'''

from pyserver import BluetoothServer
from playsound import playsound
import pygame

class LightServer(BluetoothServer):

    def __init__(self):

        BluetoothServer.__init__(self)
        
        self.count = 0

    def handleMessage(self, message):
        print()
#        self.send('LOW' if int(message) < 50 else 'HIGH')
#        self.count = self.count+1
#        self.send(str(self.count))
        
    def handleReady(self, message): 
    	print()

if __name__ == '__main__':
	server = LightServer()
	# playsound('renegade.mp3')
	pygame.mixer.init()
	pygame.mixer.music.load("renegade.mp3")
	pygame.mixer.music.play()
	server.start()