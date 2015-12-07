import os.path
import cv2
import numpy as np
class DistanceMeter:
	def __init__(self, filename='distance.dat'):
		self._a=0
		self._b=0
		self._filename=filename
		if(os.path.isfile(filename)):
			with open(filename, 'r') as f:
				self._a=float(f.readline())
				self._b=float(f.readline())
	def train(self, dist1=15.0, dist2=30.0):
		cap=cv2.VideoCapture(0)
		cdata=[]
		for j in range(2):
			while(True):
				n=0
				r=[]
				mr=0
				ret, cimg = cap.read()
				img=cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
				img = cv2.medianBlur(img,7)
				circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 500)
				if(not(circles is None)):
					circles = np.uint16(np.around(circles))
					for i in circles[0,:]:
						if(n<30):
							n=n+1
							r.append(i[2])
							mr=sum(r)/n
						else:
							r.append(i[2])
							r.remove(r[0])
							mr=sum(r)/n
						cv2.circle(cimg, (i[0], i[1]), mr,(0, 255, 0), 2)
						cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)		
				cv2.imshow("Camera", cimg)
				t=cv2.waitKey(10)
				if t&0xFF==ord('t'):
					print(mr)
					cdata.append(mr)
					break
		self._a=(dist1-dist2)*cdata[0]*cdata[1]/(cdata[1]-cdata[0])
		self._b=dist1-self._a/cdata[0]
		with open(self._filename, 'w') as f:
			f.write(str(self._a))
			f.write('\n')
			f.write(str(self._b))
		cap.release()
		cv2.destroyAllWindows()
	def getDistance(self, size):
		if (self._a!=0)and(self._b!=0):
			return self._a/float(size)+self._b
		else:
			return -1

