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
# mac_addrs = ["24:62:ab:d5:08:06","24:62:ab:d7:59:a4"]
mac_addrs = ["24:62:ab:d7:59:a4"]

writers = {}
setup = btle.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
for mac in mac_addrs:
	esp32 = btle.Peripheral(mac)
	setupService = esp32.getServiceByUUID(setup)
	writing = btle.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
	writers[mac] = (setupService.getCharacteristics(writing)[0])






# 3.457 is when renegade starts in the song
# 5.274 is when it is matched up with the first LED ON
# 1.817 second delay seems to be ocurring
delay = 1.817


# Audio
with open('renegade.csv') as csvfile:
	csv_reader = csv.DictReader(csvfile)
# # print("Time Before Playing: " + str(time.time()))
	# pygame.mixer.init()
	# pygame.mixer.music.load("renegade.mp3")
	# pygame.mixer.music.play()
	start_time = time.time() + delay



# 	print("Starting loop through csv")

	for row in csv_reader:
		current_time = time.time()
		time_diff = current_time - start_time
		time_stamp = float(row.get('timestamp'))

	#		print("Time Diff: " + str(time_diff))
	#		print("timestamp: " + str(time_stamp))

		while time_diff < time_stamp:
			current_time = time.time()
			time_diff = current_time - start_time
		for mac in row.get('mac').split('_'):
			if mac in writers:
				if row.get('led') == 'on':
					print("Turning Light on "+mac)
					writers[mac].write("A")
				else:
					print("Turning Light off "+mac)
					writers[mac].write("B")


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


	# pygame.mixer.fadeout(1000)
