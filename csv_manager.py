# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 00:24:53 2020

@author: russe
"""
import csv


def getLightsAndTimes(file = "renegade.csv"): 
    times = []
    lights = []
    with open(file) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            times.append(float(row.get('timestamp')))
            lights.append(row.get('led'))
    return lights, times

# Converts outputted csv from front-end into listst used by server
def getLightsAndTimesFeroze(file="frontend_example.csv", initial_state, color2char):
    updated_state = lst(initial_state)
    prev_time = 0
    times = []
    lights = []
    with open(file) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            time = float(row.get('TIME'))

            # Saves combined changes for previous time stamp
            if time > prev_time:
                times.append(prev_time)
                lights.append(''.join(updated_state))
                prev_time = time

            light_index = int(row.get('ID')) - 1
            color = row.get('COLOR')
            color_letter = color2char.get(color)

            if color_letter is None:
                print("Color: " + color + " is not in color_map.csv")
                return lights, times

            updated_state[light_index] = color_letter

    # Saves combined changes for last time stamp
    times.append(prev_time)
    lights.append(''.join(updated_state))

    return lights, times

def getColorInfo(file = "color_map.csv"): 
    color2char = {} 
    char2rgb = "col:" #string to be sent to app containing
    with open(file) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            color2char[row.get('Color')] = row.get('Key')
            char2rgb += row.get('Key')+row.get('RGB')+"_" #protocol for sending color map
    char2rgb = char2rgb[:-1]
    return color2char, char2rgb

def getTouchInfo(file = "touch_map.csv"):
    index2color = {} 
    with open(file) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            index2color[row.get('Touch')] = row.get('Response')
    return index2color

print(getTouchInfo())
    
            
    