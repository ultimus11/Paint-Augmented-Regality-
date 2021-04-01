import numpy as np
import cv2 as cv
import time
from pynput.mouse import Button, Controller
from random import randint

mouse=Controller()

cap = cv.VideoCapture(0)

# cap.set(3, 1280)
# cap.set(4, 720)
cap.set(3, 640)
cap.set(4, 480)
# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
x, y, w, h = 300, 200, 50, 40
track_window = (x, y, w, h)
x1, y1, w1, h1 = 400, 200, 50, 40
track_window1 = (x1, y1, w1, h1)
cv.imshow('img2',frame)
while True:
	k = cv.waitKey(1) & 0xFF
	#print(k,ord("s"))
	ret,frame = cap.read()
	frame = cv.flip(frame,1)
	if ret==True:
		# setup initial location of window
		x, y, w, h = 300, 200, 50, 40 # simply hardcoded the values
		track_window = (x, y, w, h)
		x1, y1, w1, h1 = 400, 200, 50, 40
		track_window1 = (x1, y1, w1, h1)
		img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)
		img2 = cv.rectangle(img2, (x1,y1), (x1+w1,y1+h1), 255,2)
		cv.imshow('img2',img2)
		if k == ord('s'):
			#print("S")
			break
cv.destroyWindow("img2")

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
#the MOSSE (Minimum Output Sum of Squared Error) tracker
#Discriminative Correlation Filter with Channel and Spatial Reliability 

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == trackerTypes[0]:
    tracker = cv.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]:
    tracker = cv.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv.TrackerCSRT_create()
  else:
    tracker = None
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)

  return tracker

## Select boxes
bboxes = []
colors = []
colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
# bboxes.append(track_window)
# Specify the tracker type
trackerType = "CSRT"

# Create MultiTracker object
multiTracker = cv.MultiTracker_create()

# Initialize MultiTracker
multiTracker.add(createTrackerByName(trackerType), frame, track_window)
multiTracker.add(createTrackerByName(trackerType), frame, track_window1)

#
isPressed=0
# Process video and track objects
while cap.isOpened():
	success, frame = cap.read()
	if not success:
		break
	frame = cv.flip(frame,1)
	# get updated location of objects in subsequent frames
	success, boxes = multiTracker.update(frame)
	#print(boxes)
	# draw tracked objects
	for i, newbox in enumerate(boxes):
		if i==0:
			p1 = (int(newbox[0]), int(newbox[1]))
			p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
			mouse.position=(int(newbox[0]),int(newbox[1]))
			cv.rectangle(frame, p1, p2, colors[i], 2, 1)
		if i==1:
			p3 = (int(newbox[0]), int(newbox[1]))
			p4 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
			#mouse.position=(int(newbox[0]),int(newbox[1]))
			cv.rectangle(frame, p3, p4, colors[i], 2, 1)
			if (p1[0]<=p3[0]-70):
				print("should be pressed")
				if isPressed==0:
					print("press")
					mouse.press(Button.left)
					isPressed=1
			else:
				print("should be released")
				if isPressed==1:
					print("release")
					mouse.release(Button.left)
					isPressed=0

	# x1,y1,w1,h1 = box
	# cv.rectangle(frame, (x1,y1), (x1+w1,y1+h1), 255,2)
	# # show frame
	cv.imshow('MultiTracker', frame)


	# quit on ESC button
	if cv.waitKey(1) & 0xFF == 27:  # Esc pressed
		break