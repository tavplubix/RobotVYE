from MyIntervalSlider import MyIntervalSlider
from ColorIntervalWidget import ColorIntervalWidget
import sys
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

slider = MyIntervalSlider()
slider.setMinimum(0);
slider.setMaximum(255);
slider.setLowerValue(42);
slider.setUpperValue(142);
layout.addWidget(slider)

label = QLabel()
layout.addWidget(label)

def labelSlot(val) :
    lower = slider._options.lowerValue()
    upper = slider._options.upperValue()
    s = "Lower value: " + str(lower) + " Upper value: " + str(upper)
    label.setText(s)

slider.valueChanged.connect(labelSlot)

ciw = ColorIntervalWidget()
layout.addWidget(ciw)

r = ciw.red()

frame = cv2.imread("test.jpg")
qpm = cvMatToQPixmap(frame)
label.setPixmap(qpm)

cvm = qPixmapToCvMat(qpm)
cv2.imshow("qpm to cvmat test",cvm);
k = cv2.waitKey(10)


window.show()
app.exec();
