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
    
            
    