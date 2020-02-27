#! /usr/bin/python

from bluepy import btle
import binascii
import time

# Audio
import pygame

print "Connecting..."
esp32 = btle.Peripheral("24:62:ab:d5:08:06")

print "Services..."
for svc in esp32.services:
	print str(svc)

setup = btle.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

setupService = esp32.getServiceByUUID(setup)


writing = btle.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")


writingService = setupService.getCharacteristics(writing)[0]


# Audio
pygame.mixer.init()
pygame.mixer.music.load("renegade.mp3")
pygame.mixer.music.play()


while True:
	writingService.write("A")
	print "LED ON"

	time.sleep(2)

	writingService.write("B")
	print "LED OFF"

	time.sleep(2)