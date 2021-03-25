import numpy as np
import cv2 as cv
import time
from pynput.mouse import Button, Controller
mouse=Controller()

cap = cv.VideoCapture(0)

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
x, y, w, h = 300, 200, 30, 30
track_window = (x, y, w, h)
x1, y1, w1, h1 = 400, 200, 30, 30
track_window1 = (x1, y1, w1, h1)
cv.imshow('img2',frame)
while True:
    k = cv.waitKey(1) & 0xFF
    print(k,ord("s"))
    ret,frame = cap.read()
    frame = cv.flip(frame,1)
    if ret==True:
        # setup initial location of window
        x, y, w, h = 300, 200, 30, 30 # simply hardcoded the values
        track_window = (x, y, w, h)
        x1, y1, w1, h1 = 400, 200, 30, 30
        track_window1 = (x1, y1, w1, h1)
        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        img2 = cv.rectangle(img2, (x1,y1), (x1+w1,y1+h1), 255,2)
        cv.imshow('img2',img2)
        if k == ord('s'):
            print("S")
            break

cv.destroyWindow("img2")
# set up the ROI for tracking
roi = frame[y:y+h, x:x+w]
hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )


roi1 = frame[y1:y1+h1, x1:x1+w1]
hsv_roi1 =  cv.cvtColor(roi1, cv.COLOR_BGR2HSV)
mask1 = cv.inRange(hsv_roi1, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist1 = cv.calcHist([hsv_roi1],[0],mask1,[180],[0,180])
cv.normalize(roi_hist1,roi_hist1,0,255,cv.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit1 = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )
order=2
cv.imshow('img3',frame)
while(1):
    t = cv.waitKey(1)
    ret, frame = cap.read()
    if ret == True:
        frame = cv.flip(frame,1)

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv.meanShift(dst, track_window, term_crit)

        # for the second track window 
        hsv1 = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst1 = cv.calcBackProject([hsv1],[0],roi_hist1,[0,180],1)
        ret1, track_window1 = cv.meanShift(dst1, track_window1, term_crit1)
        # Draw it on image
        x,y,w,h = track_window
        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)

        #mouse movements
        mouse.position=(x,y)
        #for the second window :
        x1,y1,w1,h1 = track_window1
    
        img2 = cv.rectangle(frame, (x1,y1), (x1+w1,y1+h1), 255,2)
        cv.imshow('img3',img2)

        if t == 27:
            break
        # if k==ord("c"):
        #     order=1
        # else:
        #     order=0
    else:
        break