from MyIntervalSlider import MyIntervalSlider
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget
import numpy



class ColorIntervalWidget(QWidget) :
    _components = (0, 1, 2)
    _componentsDict = {0 : 'Red', 1 : 'Green', 2 : 'Blue'}
    _layout = None
    _sliders = list()
    _colorLabels = list()

    def __constructQWidgets(self) :
        self._layout = QGridLayout(self)
        self.__initializeTextLabels()
        self.__initializeColorLabels()
        self.__initializeSliders()
        
    
    def __initializeSliders(self) :
        for i in self._components :
            slider = MyIntervalSlider()
            self._sliders.append(slider)
        universalSlot = lambda n : lambda val: self.__valueChangedSlot(n, val)
        for i in self._components :
            slider = self._sliders[i]
            slider.valueChanged.connect(universalSlot(i))
            slider.valueChanged.connect(universalSlot(3))
            
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.setLowerValue(0);
            slider.setUpperValue(255);
            slider.setOrientation(Qt.Horizontal)

            self._sliders.append(slider)
            self._layout.addWidget(slider, i, 1)

    def __initializeTextLabels(self) :
        for i in self._components :
            s = self._componentsDict[i] + ' component: '
            self._layout.addWidget(QLabel(s, self), i, 0)
        self._layout.addWidget(QLabel('Color: ', self), 3, 0)

    def __initializeColorLabels(self) :
        for i in self._components + (3, ) :
            label = QLabel('test', self)
            self._colorLabels.append(label)
            self._layout.addWidget(label, i, 2)
        

    def __init__(self) :
        super(QWidget, self).__init__()
        self.__constructQWidgets()
        self.setMinimumHeight(150)
        self.setMaximumHeight(150)

    def invert(self, color) :
        inverted = QColor()
        inverted.setRed(255 - color.red());
        inverted.setGreen(255 - color.green());
        inverted.setBlue(255 - color.blue());
        return inverted;

    def __valueChangedSlot(self, i, val) :
        lowerColor = self.qLower()
        upperColor = self.qUpper()
        if i != 3 :
            if i != 0 :
                lowerColor.setRed(0)
                upperColor.setRed(0)
            if i != 1 :
                lowerColor.setGreen(0)
                upperColor.setGreen(0)
            if i != 2 :
                lowerColor.setBlue(0)
                upperColor.setBlue(0)
        self.__redrawColorLabel(self._colorLabels[i], lowerColor, upperColor)

    def __redrawColorLabel(self, label, lc, uc) :
        pixmap = QPixmap(101, 26)
        painter = QPainter(pixmap)
        lowerColorRect = QRect(0, 0, 50, 25)
        upperColorRect = QRect(50, 0, 50, 25)

        font = QFont('Times', 11)
        painter.setFont(font)

        painter.setPen(Qt.black);
        painter.setBrush(lc);
        painter.drawRect(lowerColorRect);
        lgray = lc.red() + lc.green() + lc.blue();
        painter.setPen(self.invert(lc));
        painter.drawText(lowerColorRect.translated(8, 2), 0, str(lgray));

        painter.setPen(Qt.black);
        painter.setBrush(uc);
        painter.drawRect(upperColorRect);
        ugray = uc.red() + uc.green() + uc.blue();
        painter.setPen(self.invert(uc));
        painter.drawText(upperColorRect.translated(8, 2), 0, str(ugray));
        del painter

        label.setPixmap(pixmap);


    def red(self) :
        return (self._sliders[0].lowerValue(), self._sliders[0].upperValue())

    def green(self) :
        return (self._sliders[1].lowerValue(), self._sliders[1].upperValue())

    def blue(self) :
        return (self._sliders[2].lowerValue(), self._sliders[2].upperValue())

    def qLower(self) :
        color = QColor()
        color.setRed(self._sliders[0].lowerValue())
        color.setGreen(self._sliders[1].lowerValue())
        color.setBlue(self._sliders[2].lowerValue())
        return color

    def qUpper(self) :
        color = QColor()
        color.setRed(self._sliders[0].upperValue())
        color.setGreen(self._sliders[1].upperValue())
        color.setBlue(self._sliders[2].upperValue())
        return color

    def npLower(self) :
        color = list()
        for i in self._components :
            color.append(self._sliders[i].lowerValue())
        return numpy.array(color, dtype = 'uint8')

    def npUpper(self) :
        color = list()
        for i in self._components :
            color.append(self._sliders[i].upperValue())
        return numpy.array(color, dtype = 'uint8')
