#!/usr/bin/python3

import sys
import time
# Audio Import
import pygame
# CSV Import
import csv
from getkey import getkey, keys

if len(sys.argv)!= 3:
	print("\nPlease call the program using:")
	print("\t python test_server.py audio_file.mp3 timing_file.csv\n")
	exit()

audio_file_input = sys.argv[1]
csv_file_input = sys.argv[2]

# 3.457 is when renegade starts in the song
# 5.274 is when it is matched up with the first LED ON
# 1.817 second delay seems to be ocurring
delay = 0


# Audio
with open(csv_file_input) as csvfile:
	csv_reader = csv.DictReader(csvfile)
# print("Time Before Playing: " + str(time.time()))
	pygame.mixer.init()
	pygame.mixer.music.load(audio_file_input)
	pygame.mixer.music.play()
	start_time = time.time() + delay


# 	print("Starting loop through csv")
	times = []
	lights = []

	for row in csv_reader:
		times.append(float(row.get('timestamp')))
		lights.append(row.get('led'))


	i = 0
	while i < len(times):
		current_time = time.time()
		time_diff = current_time - start_time
		time_stamp = times[i]

		while time_diff < time_stamp:
			current_time = time.time()
			time_diff = current_time - start_time

		print(lights[i])

		i += 1


# 	for row in csv_reader:
# 		current_time = time.time()
# 		time_diff = current_time - start_time
# 		time_stamp = float(row.get('timestamp'))

# #		print("Time Diff: " + str(time_diff))
# #		print("timestamp: " + str(time_stamp))
# 		# key = getkey(blocking=False)

# 		# if key == 'a':
# 		# 	print("Pressed A!")

# 		while time_diff < time_stamp:
# 			current_time = time.time()
# 			time_diff = current_time - start_time

# 			# key = getkey(blocking=False)

# 			# if key == 'a':
# 			# 	print("Pressed A!")

# 		if row.get('led') == 'on':
# 			print("on")
# 		else:
# 			print("off")


