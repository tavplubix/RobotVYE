from ColorIntervalWidget import ColorIntervalWidget
from StreamReader import *
from ObjectsDetector import *
from ObjectTracker import *
from ImageWidget import *
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from QtCV import *
import cv2
import sys


app = QApplication(sys.argv)
window = QMainWindow();
window.setMinimumWidth(900);
window.setMinimumHeight(750);
centralWidget = QWidget(window)
window.setCentralWidget(centralWidget)
layout = QVBoxLayout()
centralWidget.setLayout(layout)

ciw = ColorIntervalWidget()
layout.addWidget(ciw)

#imagew = ImageWidget(window)
#layout.addWidget(imagew)
label = QLabel('Loading...')
layout.addWidget(label)
label.setContextMenuPolicy(Qt.CustomContextMenu)

debugInfo = QLabel();
layout.addWidget(debugInfo)

stream = StreamReader()
stream.connect()
detector = ObjectDetecor()
tracker = SimpleObjectTracker(0, 0, 0)


def click(qpoint) :
    x = qpoint.x()
    y = qpoint.y()
    tracker.setNewPosition(x, y, 50)

label.customContextMenuRequested.connect(click)

def mainLoop() :
    if stream.readable() == False :
        return
    frame = stream.getFrame();
    obj = detector.findObjects(frame, ciw.npLower(), ciw.npUpper())
    debugInfo.setText(str(obj))
    tracker.processNewPositions(obj)
    x, y, r = tracker.position();
    cv2.circle(frame, (int(x), int(y)), int(r), (0, 0, 255), 3)

    #imagew.setCvImage(frame)

    #mask = cv2.inRange(frame, ciw.npLower(), ciw.npUpper())
    #result = cv2.bitwise_and(frame, frame, mask = mask)
    result = frame

    #width = 800 #centralWidget.width() - 10
    #height = 600 #centralWidget.height() - ciw.height() - 10
    qpm = cvMatToQPixmap(result) #cvMatToQPixmap(result).scaled(width, height, Qt.KeepAspectRatio)
    label.setPixmap(qpm)
    label.resize(qpm.size())

timer = QTimer()
timer.setInterval(100)
timer.timeout.connect(mainLoop)
timer.start()


window.show()
app.exec();
stream.close()
