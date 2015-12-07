from MyIntervalSlider import MyIntervalSlider
from AbstractColorIntervalWidget import *

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget

import numpy



class HSVIntervalWidget(AbstractColorIntervalWidget) :

    def __init__(self, parent = None) :
        self._components = (0, 1, 2)
        self._componentsDict = {0 : 'Hue', 1 : 'Saturation', 2 : 'Value'}
        self._slidersValues = ((0, 179), (0, 255), (0, 255))
        super(HSVIntervalWidget, self).__init__(parent)

    def _valueChangedSlot(self, i, val) :
        lowerColor = self.qLower()
        upperColor = self.qUpper()
        lowerValue = upperValue = 0
        if i == 0 :
             lowerValue = lowerColor.hue()
             upperValue = upperColor.hue()
             lowerColor.setHsv(lowerValue * 2 + 1, 255, 128)
             upperColor.setHsv(upperValue * 2 + 1, 255, 128)
        if i == 1 :
            lowerValue = lowerColor.saturation()
            upperValue = upperColor.saturation()
            lowerColor.setHsv(0, lowerValue, 128)
            upperColor.setHsv(0, upperValue, 128)
        if i == 2 :    
            lowerValue = lowerColor.value()
            upperValue = upperColor.value()  
            lowerColor.setHsv(0, 255, lowerValue)
            upperColor.setHsv(0, 255, upperValue)
        self._redrawColorLabel(i, lowerColor, upperColor, lowerValue, upperValue)



    def hue(self) :
        return self.component(0)
    def saturation(self) :
        return self.component(1)
    def value(self) :
        return self.component(2)

    def qLower(self) :
        color = QColor()
        color.setHsv(self.component(0)[0] * 2 + 1, self.component(1)[0], self.component(2)[0])
        return color

    def qUpper(self) :
        color = QColor()
        color.setHsv(self.component(0)[1] * 2 + 1, self.component(1)[1], self.component(2)[1])
        return color

    


class RGBIntervalWidget(AbstractColorIntervalWidget) :

    def __init__(self, parent = None) :
        self._components = (0, 1, 2)
        self._componentsDict = {0 : 'Red', 1 : 'Green', 2 : 'Blue'}
        self._slidersValues = ((0, 255), (0, 255), (0, 255))
        super(RGBIntervalWidget, self).__init__(parent)

    def _valueChangedSlot(self, i, val) :
        lowerColor = self.qLower()
        upperColor = self.qUpper()
        if i == 0 :
             lowerColor.setRgb(lowerColor.red(), 0, 0)
             upperColor.setRgb(upperColor.red(), 0, 0)
        if i == 1 :        
             lowerColor.setRgb(0, lowerColor.green(), 0)
             upperColor.setRgb(0, upperColor.green(), 0)
        if i == 2 :      
             lowerColor.setRgb(0, 0, lowerColor.blue())
             upperColor.setRgb(0, 0, upperColor.blue())
        lgray = lowerColor.red() + lowerColor.green() + lowerColor.blue();
        ugray = upperColor.red() + upperColor.green() + upperColor.blue();
        self._redrawColorLabel(i, lowerColor, upperColor, lgray, ugray)

    def red(self) :
        return self.component(0)
    def green(self) :
        return self.component(1)
    def blue(self) :
        return self.component(2)

    def qLower(self) :
        color = QColor()
        color.setRed(self.component(0)[0])
        color.setGreen(self.component(1)[0])
        color.setBlue(self.component(2)[0])
        return color

    def qUpper(self) :
        color = QColor()
        color.setRed(self.component(0)[1])
        color.setGreen(self.component(1)[1])
        color.setBlue(self.component(2)[1])
        return color









