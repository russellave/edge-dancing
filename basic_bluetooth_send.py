#! /usr/bin/python

from bluepy import btle
import binascii
import time

# Audio
import pygame

# CSV
import csv

	# for row in reader:
	# 	print(row['first_name'], row['last_name'])

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
with open('renegade.csv') as csvfile:
	csv_reader = csv.DictReader(csvfile)
# print("Time Before Playing: " + str(time.time()))
	pygame.mixer.init()
	pygame.mixer.music.load("renegade.mp3")
	pygame.mixer.music.play()
	start_time = time.time()

	print("Starting loop through csv")

	for row in csv_reader:
		current_time = time.time()
		time_diff = current_time - start_time
		time_stamp = row.get('timestamp')

		print("Time Diff: " + str(time_diff))
		print("timestamp: " + time_stamp)

		while time_diff < time_stamp:
			current_time = time.time()
			time_diff = current_time - start_time

		if row.get('led') == 'on':
			print("Turning Light on")
			writingService.write("A")
		else:
			print("Turning Light off")
			writingService.write("B")


# # while True:
# print("Time of next loop: "  + str(time.time()))
# time.sleep(3.447)
# writingService.write("A")
# print "LED ON"

# # 4.25
# time.sleep(0.833)

# writingService.write("B")
# print "LED OFF"

# # 5.042
# time.sleep(0.792)
# writingService.write("A")
# print "LED ON"

# time.sleep(1)

# writingService.write("B")
# print "LED OFF"


	pygame.mixer.fadeout(1000)