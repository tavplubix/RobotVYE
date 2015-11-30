from ColorIntervalWidget import ColorIntervalWidget
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from QtCV import *
import cv2

app = QApplication(sys.argv)
window = QMainWindow();
window.setMinimumWidth(500);
window.setMinimumHeight(500);
centralWidget = QWidget(window)
window.setCentralWidget(centralWidget)
layout = QVBoxLayout()
centralWidget.setLayout(layout)

ciw = ColorIntervalWidget()
layout.addWidget(ciw)

label = QLabel('Result')
layout.addWidget(label)

cap = cv2.VideoCapture(0)

def mainLoop() :
    retVal, frame = cap.read();
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(frame, ciw.npLower(), ciw.npUpper())
    result = cv2.bitwise_and(frame, frame, mask = mask)
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
