from MyIntervalSlider import MyIntervalSlider
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel


app = QApplication(sys.argv)
window = QMainWindow();
window.setMinimumWidth(100);
window.setMinimumHeight(100);
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


window.show()
app.exec();
