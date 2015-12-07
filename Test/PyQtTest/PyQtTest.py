#Import classes from this project
from ColorIntervalWidgets import *
from StreamReader import *
from ObjectsDetector import *
from ObjectTracker import *
from QtCV import *
#Import standart modules
import sys
#Import OpenCV module
import cv2
#Import Qt classes
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel



app = QApplication(sys.argv)
window = QMainWindow();
window.setMinimumWidth(900);
window.setMinimumHeight(750);
centralWidget = QWidget(window)
window.setCentralWidget(centralWidget)
layout = QVBoxLayout()
centralWidget.setLayout(layout)

ciw = HSVIntervalWidget(window)
layout.addWidget(ciw)

imageLabel = QLabel('Loading...')
layout.addWidget(imageLabel)

debugInfo = QLabel();
layout.addWidget(debugInfo)

stream = StreamReader()
detector = ObjectDetecor()
tracker = ObjectTracker()

#Select object at the position qpoint 
def click(qpoint) :
    x = qpoint.x()
    y = qpoint.y()
    tracker.setTrackingObject(x, y, 50)

#In case of right click on label, call click() (almost hack)
imageLabel.setContextMenuPolicy(Qt.CustomContextMenu)
imageLabel.customContextMenuRequested.connect(click)

def mainLoop() :
    if stream.readable() == False :
        return
    frame = stream.getFrame();
    objects = detector.findObjects(frame, ciw.npLower(), ciw.npUpper())
    debugInfo.setText(str(objects))
    tracker.processNewPositions(objects)
    x, y, r = tracker.objectPosition();
    if x >= 0 and y >= 0 and r >= 0 :
        cv2.circle(frame, (int(x), int(y)), int(r), (0, 0, 255), 3)

    #mask = cv2.inRange(frame, ciw.npLower(), ciw.npUpper())
    #result = cv2.bitwise_and(frame, frame, mask = mask)
    result = frame

    #width = 800 #centralWidget.width() - 10
    #height = 600 #centralWidget.height() - ciw.height() - 10
    qpm = cvMatToQPixmap(result) #cvMatToQPixmap(result).scaled(width, height, Qt.KeepAspectRatio)
    imageLabel.setPixmap(qpm)
    imageLabel.resize(qpm.size())

#This timer calls mainLoop() every 100 ms
timer = QTimer()
timer.setInterval(100)
timer.timeout.connect(mainLoop)
timer.start()


window.show()

#Enter in main Qt event loop
app.exec();
