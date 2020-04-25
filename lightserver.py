#!/usr/bin/python3
'''
Subclasses BluetoothSocket to serve messages "LOW" and "HIGH" based on values received from
client

Copyright Simon D. Levy 2018

MIT License
'''

from pyserver import BluetoothServer
from csv_manager import getTouchInfo, getPoseInfo

import sys
import numpy as np
import imutils
import os
import cv2


BUTTON_COLOR_DURATION = 2


class LightServer(BluetoothServer):

    def __init__(self):

        BluetoothServer.__init__(self)
        
        self.count = 0
        self.touch2out = getTouchInfo()
        self.pose2out = getPoseInfo()
        self.temps = self.init_temps()

    # Assuming s is index of color being changed
    def handleTouch(self, s, curr_state, current_time, input_times):
        try: 
            out = self.touch2out[s]
            lst = list(curr_state)
            lst[int(s)-1]  = out #-1 because s is 1 indexed
            out_str = ''.join(lst)

            input_times[int(s)-1] = current_time + BUTTON_COLOR_DURATION

            self.send(out_str)
        except: 
            out_str = curr_state
        return out_str, input_times

        
    def temp_matching_mult(self,img_edge, template_edge, visualize = True):
    # load the image image, convert it to grayscale, and detect edges
        (tH, tW) = template_edge.shape[:2]
        threshold = .03
    #    metric_threshold = .5
        max_metric = 0
    #    result = cv2.matchTemplate(img_edge, template_edge,cv2.TM_CCOEFF_NORMED)
    #    result = np.max(result)
    #    if result>threshold: 
    #        return True, result
    #    return False, result
        for scale in np.linspace(.3, 1.0, 20)[::-1]:
            resized = imutils.resize(img_edge, width = int(img_edge.shape[1] * scale))
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break
           
            result = cv2.matchTemplate(img_edge, template_edge, cv2.TM_CCOEFF_NORMED)
            result = np.max(np.abs(result))
            if(result>max_metric): 
                max_metric = result
        return max_metric>threshold, max_metric
    
    def process_img_no_load(self,img): 
    #    if is_bs: 
    #        img = bs.apply(img)
    #        img= cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.Canny(img, 50, 200)
        img = cv2.blur(img,(5,5))
        (thresh, img) = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY)
        return img
    
    def init_temps(self,temp_dir = 'vision\\templates'):
        temps = []
        for temp_file in os.listdir(temp_dir):
            temps.append(os.path.join(temp_dir, temp_file))
        return temps
        
    
    def doImage(self,frame):
        img = self.process_img_no_load(frame)

        is_match = False
        max_temp = 0
        for i in range(len(self.temps)):
            temp = self.temps[i]
            if temp == 'vision\\templates\\none':
                continue
            temp_img = cv2.imread(temp)
            temp_proc = self.process_img_no_load(temp_img)
#                cv2.imshow('temp', temp_proc)
            is_match, metric = self.temp_matching_mult(img, temp_proc)
            if metric> max_temp:
                max_temp = metric
                max_temp_index = i
        if(is_match):
            print(self.temps[max_temp_index].split('\\')[2].split('.')[0]+ ' is match!')
            is_match = False
            self.send(self.pose2out[self.temps[max_temp_index].split('\\')[2]])
            
#        font                   = cv2.FONT_HERSHEY_SIMPLEX
#        bottomLeftCornerOfText = (10,400)
#        fontScale              = 1
#        fontColor              = (255,0,0)
#        lineType               = 5
#        cv2.putText(img,self.temps[max_temp_index].split('\\')[2].split('.')[0]+' '+str(metric) + ' is highest', 
#            bottomLeftCornerOfText, 
#            font, 
#            fontScale,
#            fontColor,
#            lineType)
            
        cv2.imshow('refresh', img)
        


if __name__ == '__main__':
#    if len(sys.argv)!= 3:


    audio_file_input = "every_time_we_touch.mp3"
    csv_file_input = "everytime_we_touch.csv"

    server = LightServer()

    server.start(audio_file_input, csv_file_input)
    # server.start()

