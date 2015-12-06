﻿# import the necessary packages
from collections import deque
import numpy as np
import argparse
import distance
#import imutils
import cv2
dm=distance.DistanceMeter()
def nothing(x):
	pass

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

#trackbars 'n' preview
#prewiew images
low = np.zeros((128,256,3), np.uint8)
up = np.zeros((128,256,3), np.uint8)
cv2.namedWindow("Lower")
cv2.namedWindow("Upper")

#trackbars
cv2.createTrackbar('H','Lower',0,255,nothing)
cv2.setTrackbarPos('H', 'Lower', 95)
cv2.createTrackbar('S','Lower',0,255,nothing)
cv2.setTrackbarPos('S', 'Lower', 45)
cv2.createTrackbar('V','Lower',0,255,nothing)
cv2.setTrackbarPos('V', 'Lower', 19)

cv2.createTrackbar('H','Upper',0,255,nothing)
cv2.setTrackbarPos('H', 'Upper', 137)
cv2.createTrackbar('S','Upper',0,255,nothing)
cv2.setTrackbarPos('S', 'Upper', 255)
cv2.createTrackbar('V','Upper',0,255,nothing)
cv2.setTrackbarPos('V', 'Upper', 255)
#origal code
#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)

#non-original code
#greenLower = (25,0,0)
#greenUpper = (130,255,60)

pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
 
	# get colors from trackbars and make border arrays
	hl = cv2.getTrackbarPos('H','Lower')
	sl = cv2.getTrackbarPos('S','Lower')
	vl = cv2.getTrackbarPos('V','Lower')

	hu = cv2.getTrackbarPos('H','Upper')
	su = cv2.getTrackbarPos('S','Upper')
	vu = cv2.getTrackbarPos('V','Upper')

    #preview
	low[:] = [hl,sl,vl]
	up[:] = [hu,su,vu]

	low = cv2.cvtColor(low, cv2.COLOR_HSV2BGR)
	up = cv2.cvtColor(up, cv2.COLOR_HSV2BGR)

	# define range
	#lower = (25,0,0)
	#upper = (130,255,60)
	lower = np.array([hl,sl,vl])
	upper = np.array([hu,su,vu])

	# resize the frame, blur it, and convert it to the HSV
	# color space
	height, width, channels = frame.shape
	k=float(width)/600.0
	frame = cv2.resize(frame, (0, 0), fx=k, fy=k)
	blurred = cv2.GaussianBlur(frame, (13, 13), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 30:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			dist=dm.getDistance(radius)
			cv2.putText(frame, str(dist), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255))
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# update the points queue
	pts.appendleft(center)
	
	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		#cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	cv2.imshow("Lower",low)
	cv2.imshow("Upper",up)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
