import numpy as np
import imutils
import cv2
import os

import time

def temp_matching_mult(img_edge, template_edge, visualize = True):
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
    for scale in np.linspace(.5, 1.0, 10)[::-1]:
        resized = imutils.resize(img_edge, width = int(img_edge.shape[1] * scale))
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break
       
        result = cv2.matchTemplate(img_edge, template_edge, cv2.TM_CCOEFF_NORMED)
        result = np.max(np.abs(result))
        if(result>max_metric): 
            max_metric = result
    return max_metric>threshold, max_metric

def process_img_no_load(img): 
#    if is_bs: 
#        img = bs.apply(img)
#        img= cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.Canny(img, 50, 200)
    img = cv2.blur(img,(5,5))
    (thresh, img) = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY)
    return img

def init_temps(temp_dir = 'templates'):
    temps = []
    for temp_file in os.listdir(temp_dir):
        temps.append(os.path.join(temp_dir, temp_file))
    return temps


def do_image(frame): 
    img = process_img_no_load(frame)

    is_match = False
    max_temp = 0
    for i in range(len(temps)):
        temp = temps[i]
        if temp == 'templates\\none':
            continue
        temp_img = cv2.imread(temp)
        temp_proc = process_img_no_load(temp_img)
#                cv2.imshow('temp', temp_proc)
        is_match, metric = temp_matching_mult(img,temp_proc)
        if metric> max_temp:
            max_temp = metric
            max_temp_index = i
    if(is_match):
        print(temps[max_temp_index].split('\\')[1].split('.')[0]+ ' is match!')
        is_match = False
        
#    font                   = cv2.FONT_HERSHEY_SIMPLEX
#    bottomLeftCornerOfText = (10,400)
#    fontScale              = 1
#    fontColor              = (255,0,0)
#    lineType               = 5
#    cv2.putText(frame,temps[max_temp_index].split('\\')[1].split('.')[0]+' '+str(metric) + ' is highest', 
#        bottomLeftCornerOfText, 
#        font, 
#        fontScale,
#        fontColor,
#        lineType)
#        
#    cv2.imshow('refresh', frame)
#    cv2.imshow('proc',img)   
    
if __name__ == "__main__":
    temps= init_temps()
    temps.append("templates\\none")
    max_temp_index = -1
    max_temp = 0
    cap = cv2.VideoCapture(0)
    refresh_rate = 30
    frame_count = 0

    while(True):
        
        ret, frame = cap.read()
        if frame_count == 0: 
            start = time.time()
            do_image(frame)
            end = time.time()
            print(end-start)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
        frame_count = (frame_count +1)%refresh_rate

    cap.release()
    cv2.destroyAllWindows()



