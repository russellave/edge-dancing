#! /usr/bin/python

from bluepy import btle

print "Connecting..."
dev = btle.Peripheral("24:62:ab:d5:08:06")

print "Services..."
for svc in dev.services:
	print str(svc)
