# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:28:51 2020

@author: russe
"""
import cv2 


def init_temps(temp_dir = 'templates'):
    temps = []
    for temp_file in os.listdir(temp_dir):
        temps.append(os.path.join(temp_dir, temp_file))
    return temps

def process_img_no_load(img, bs, is_bs, kernel = 0): 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if bs: 
        img = bs.apply(img)
#        img= cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.Canny(img, 75, 275)

    img = cv2.blur(img,(5,5))
    (thresh, img) = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY)
#    img = img.apply(img); 

    return img

while(True):
    cap = cv2.VideoCapture(0)    
    temps = init_temps()
    fgbg2 = cv2.createBackgroundSubtractorMOG2(); 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3));
#    ret, frame = cap.read()
#    img = process_img_no_load(frame, fgbg2, True, kernel)
#    cv2.imshow('refresh', img)
    is_match = False
    for i in range(len(temps)):
        temp = temps[i]
        if temp == 'templates\\none':
            continue
        temp_img = cv2.imread(temp)
        temp_proc = process_img_no_load(temp_img, 0, False)
        cv2.imshow(temp, temp_proc)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()