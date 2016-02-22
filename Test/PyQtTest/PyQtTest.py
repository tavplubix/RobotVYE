#Import standart modules
import sys
#Import classes from this project
sys.path.append('./GUI')
from ColorIntervalWidgets import *
from StreamReader import *
from ObjectsDetector import *
from SimpleObjectTracker import *
from ImageWidget import *
from QtCV import *
#Import OpenCV module
import cv2
#Import Qt classes
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QComboBox



app = QApplication(sys.argv)
window = QMainWindow();
window.setMinimumWidth(900);
window.setMinimumHeight(750);
centralWidget = QWidget(window)
window.setCentralWidget(centralWidget)
layout = QGridLayout()
centralWidget.setLayout(layout)

colorspaceComboBox = QComboBox(window)
colorspaceComboBox.addItems(['HSV', 'RGB'])
layout.addWidget(colorspaceComboBox)

ciw = HSVIntervalWidget(window)
layout.addWidget(ciw)

def changeColorspace(s) :
    global ciw
    global layout
    #layout.removeWidget(ciw)
    ciw.destroy()
    del ciw
    
    if s == 0 :
        ciw = HSVIntervalWidget(window)
    elif s == 1 :
        ciw = RGBIntervalWidget(window)
    else :
        print('WARNING: changeColorspace()')
    layout.addWidget(ciw, 1, 0)
    #layout.replaceWidget(ciw, imageLabel)
colorspaceComboBox.activated.connect(changeColorspace)

imageLabel = QLabel('Loading...')
layout.addWidget(imageLabel)

#debugInfo = QLabel();
#layout.addWidget(debugInfo)

stream = StreamReader()
stream.connect()
detector = ObjectDetecor()
tracker = SimpleObjectTracker(0, 0, 0)

zoom = 1
#Select object at the position qpoint 
def click(qpoint) :
    x = int(qpoint.x() / zoom)
    y = int(qpoint.y() / zoom)
    tracker.setTrackingObject(x, y, 50)

#In case of right click on label, call click() (almost hack)
imageLabel.setContextMenuPolicy(Qt.CustomContextMenu)
imageLabel.customContextMenuRequested.connect(click)

def mainLoop() :
    if stream.readable() == False :
        return
    frame = stream.getFrame();
    objects = detector.findObjects(frame, ciw.npLower(), ciw.npUpper())
    #debugInfo.setText(str(objects))
    tracker.processNewPositions(objects)
    x, y, r = tracker.objectPosition();
    if x >= 0 and y >= 0 and r >= 0 :
    cv2.circle(frame, (int(x), int(y)), int(r), (0, 0, 255), 3)

    #imagew.setCvImage(frame)

    #mask = cv2.inRange(frame, ciw.npLower(), ciw.npUpper())
    #result = cv2.bitwise_and(frame, frame, mask = mask)
    result = frame

    imageLabel.setPixmap(qpm.scaled(qpm.width() * zoom, qpm.height() * zoom, Qt.KeepAspectRatio))
    imageLabel.resize(qpm.size())

#This timer calls mainLoop() every 100 ms
timer = QTimer()
timer.setInterval(100)
timer.timeout.connect(mainLoop)
timer.start()


window.show()

#Enter in main Qt event loop
app.exec();
stream.close()
