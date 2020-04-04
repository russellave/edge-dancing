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
            
print(getLightsAndTimes())
            
    