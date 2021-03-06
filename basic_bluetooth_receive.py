#! /usr/bin/python

from bluepy import btle
import binascii

print "Connecting..."
esp32 = btle.Peripheral("24:62:ab:d5:08:06")

print "Services..."
for svc in esp32.services:
	print str(svc)

setup = btle.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

setupService = esp32.getServiceByUUID(setup)


reading = btle.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")


readingService = setupService.getCharacteristics(reading)[0]


while True:
	val = readingService.read()
	print "Received Message: " + val