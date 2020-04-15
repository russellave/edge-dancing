import numpy as np
import imutils
import cv2
import os


def temp_matching_mult(img_edge, template_edge, visualize = True):
    # load the image image, convert it to grayscale, and detect edges
    (tH, tW) = template_edge.shape[:2]
    threshold = .8
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
        print(result)
        if(result>max_metric): 
            max_metric = result
    return max_metric>threshold, max_metric

def process_img_no_load(img, bs, is_bs, kernel = 0): 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if is_bs: 
        img = bs.apply(img)
        img= cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.Canny(img, 75, 275)

    img = cv2.blur(img,(5,5))
#    ret, img = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU);

    return img

def init_temps(temp_dir = 'templates'):
    temps = []
    for temp_file in os.listdir(temp_dir):
        temps.append(os.path.join(temp_dir, temp_file))
    return temps


if __name__ == "__main__":
    temps= init_temps()
    temps.append("templates\\none")
    max_temp_index = -1
    max_temp = 0
    cap = cv2.VideoCapture(0)
    refresh_rate = 10 #check every 10 frames
    
    fgbg2 = cv2.createBackgroundSubtractorMOG2(); 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3));
    frame_count = 0

    while(True):
        ret, frame = cap.read()
#        img = process_img_no_load(frame, fgbg2, True, kernel)
        img = process_img_no_load(frame, fgbg2, True, kernel)

        is_match = False
        if frame_count == 0:  
            for i in range(len(temps)):
                temp = temps[i]
                if temp == 'templates\\none':
                    continue
                temp_img = cv2.imread(temp)
                temp_proc = process_img_no_load(temp_img, 0, False)
#                cv2.imshow('temp', temp_proc)
                is_match, metric = temp_matching_mult(img,temp_proc)
                print(metric, max_temp)
                if metric> max_temp:
                    max_temp = metric
                    max_temp_index = i
            max_temp_index = -1
            max_temp = 0
            if(is_match):
                print(temps[max_temp_index].split('\\')[1].split('.')[0]+ ' is match!')
                is_match = False
            font                   = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10,400)
            fontScale              = 1
            fontColor              = (255,0,0)
            lineType               = 5
            
        frame_count = (frame_count +1)%10
        cv2.putText(frame,temps[max_temp_index].split('\\')[1].split('.')[0]+' '+str(metric) + ' is highest', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            
        cv2.imshow('refresh', frame)
        cv2.imshow('proc',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



