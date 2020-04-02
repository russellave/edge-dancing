#!/usr/bin/python3

import time
# Audio Import
import pygame
# CSV Import
import csv


# 3.457 is when renegade starts in the song
# 5.274 is when it is matched up with the first LED ON
# 1.817 second delay seems to be ocurring
delay = 0


# Audio
with open('renegade.csv') as csvfile:
	csv_reader = csv.DictReader(csvfile)
# print("Time Before Playing: " + str(time.time()))
	pygame.mixer.init()
	pygame.mixer.music.load("renegade.mp3")
	pygame.mixer.music.play()
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

		if row.get('led') == 'on':
			print("Turning Light on")
		else:
			print("Turning Light off")