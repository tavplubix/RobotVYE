#from StreamReader import *
import numpy
import cv2


class ObjectDetecor :
    #stream = None
    #def __init__(self, stream) :
        #self.stream = stream
    minRadius = 15;
    minContourArea = 500;

    def findObjects(self, frame, npLower, npUpper) :
        #convert image and colors to HSV
        #hsvFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        #hsvLower = toHSV(qlower)
        #hsvUpper = toHSV(qupper)
        #hsvFrame = frame
        #hsvLower = toRGB(qlower)
        #hsvUpper = toRGB(qupper)

        #find all pixels with color between hsvLower and hsvUpper
        mask = cv2.inRange(frame, npLower, npUpper)
        #remove all small groups of pixels in the mask
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        #find contours in the mask
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cv2.drawContours(frame, contours, -1, (255,0,0), 1)
        objects = list()    #list of found objects
        
        #find largest contours in the mask and centers of this contours
        bigContours = [x for x in contours if cv2.contourArea(x) >= self.minContourArea]
        cv2.drawContours(frame, bigContours, -1, (0,255,0), 2)
        for c in bigContours:
            #area = cv2.contourArea(contours[0])
            #c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > self.minRadius:
                objects.append([int(x), int(y), int(radius)])
                # draw the circle and centroid on the frame
                cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 1)
                #cv2.circle(frame, center, 5, (0, 0, 255), -1)

        return objects


