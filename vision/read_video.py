# importing libraries 
import numpy as np 
import cv2 

# creating object 
#fgbg1 = cv2.bgsegm.createBackgroundSubtractorMOG(); 
fgbg2 = cv2.createBackgroundSubtractorMOG2(); kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)); 
 
#fgbg3 = cv2.bgsegm.createBackgroundSubtractorGMG(); 

# capture frames from a camera 
cap = cv2.VideoCapture(0); 
while(1): 
	# read frames 
	ret, img = cap.read(); 
	
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); cv2.imshow('gray', gray); #fgmask2 = fgbg2.apply(img);      fgmask2= cv2.morphologyEx(fgmask2, cv2.MORPH_OPEN, kernel);   canny = cv2.Canny(fgmask2, 50, 200); cv2.imshow('canny', canny);  smooth = cv2.blur(canny,(5,5)); cv2.imshow('canny smooth', smooth);#	fgmask3 = fgbg3.apply(img); 
	hsv_nemo = cv2.cvtColor(img, cv2.COLOR_RGB2HSV); cv2.imshow('hsv', hsv_nemo);
	hsv_edge = cv2.Canny(hsv_nemo, 75, 275); cv2.imshow('hsv_edge', hsv_edge); blurred = cv2.blur(hsv_edge,(5,5)); cv2.imshow('blur', blurred); 

    # Finding unknown region
    # (thresh, binimage) = cv2.threshold(smooth, 75, 255, cv2.THRESH_BINARY); cv2.imshow('bw smooth', binimage); 
	#cv2.imshow('MOG2', fgmask2);print(img.shape, fgmask2.shape, canny.shape, smooth.shape, binimage.shape)

	k = cv2.waitKey(30) & 0xff; 
	if k == 27: 
		break; 

cap.release(); 
cv2.destroyAllWindows(); 
