#! /usr/bin/python

from bluepy import btle
import binascii

print "Connecting..."
dev = btle.Peripheral("24:62:ab:d5:08:06")

print "Services..."
for svc in dev.services:
	print str(svc)

setupSensor = btle.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

setupService = dev.getServiceByUUID(setupSensor)


readingSensor = btle.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")


setupConfig = setupService.getCharacteristics(readingSensor)[0]

val = setupConfig.read()

print "Light sensor raw value", binascii.b2a_hex(val)