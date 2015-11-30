from ColorIntervalWidget import ColorIntervalWidget
from StreamReader import *
from ObjectsDetector import *
from PyQt5.QtCore import QTimer
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

label = QLabel('Loading...')
layout.addWidget(label)

debugInfo = QLabel();
layout.addWidget(debugInfo)

stream = StreamReader()

def mainLoop() :
    if stream.readable() == False :
        return
    frame = stream.getFrame();
    obj = ObjectDetecor.findObjects(frame, ciw.qLower(), ciw.qUpper())
    debugInfo.setText(str(obj))
    #mask = cv2.inRange(frame, ciw.npLower(), ciw.npUpper())
    #result = cv2.bitwise_and(frame, frame, mask = mask)
    result = frame

    width = centralWidget.width() - 10
    height = centralWidget.height() - ciw.height() - 10
    qpm = cvMatToQPixmap(result).scaled(width, height, Qt.KeepAspectRatio)
    label.setPixmap(qpm)
    label.setMinimumSize(qpm.size())

timer = QTimer()
timer.setInterval(100)
timer.timeout.connect(mainLoop)
timer.start()


window.show()
app.exec();
