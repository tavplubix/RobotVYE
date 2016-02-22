from MyIntervalSlider import MyIntervalSlider
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget
import numpy



class AbstractColorIntervalWidget(QWidget) :
    _components = None      # range(0, numberOfComponents), for example (0, 1, 2)
    _componentsDict = None  # {0 : 'First component name', 1 : 'Second component name', etc}, for example {0 : 'Red', 1 : 'Green', 2 : 'Blue'}
    _slidersValues = None
        
    def __constructQWidgets(self) :
        self.__layout = QGridLayout(self)
        self.setLayout(self.__layout)
        self.__initializeTextLabels()
        self.__initializeColorLabels()
        self.__initializeSliders()
        
    
    def __initializeSliders(self) :
        for i in self._components :
            slider = MyIntervalSlider()
            self.__sliders.append(slider)
        universalSlot = lambda n : lambda val: self._valueChangedSlot(n, val)
        for i in self._components :
            slider = self.__sliders[i]
            slider.valueChanged.connect(universalSlot(i))
            slider.valueChanged.connect(universalSlot(3))
            
            slider.setMinimum(self._slidersValues[i][0])
            slider.setMaximum(self._slidersValues[i][1])
            slider.setLowerValue(self._slidersValues[i][0]);
            slider.setUpperValue(self._slidersValues[i][1]);
            slider.setOrientation(Qt.Horizontal)

            self.__sliders.append(slider)
            self.__layout.addWidget(slider, i, 1)

    def __initializeTextLabels(self) :
        for i in self._components :
            s = self._componentsDict[i] + ' component: '
            label = QLabel(s, self)
            self.__textLabels.append(label)
            self.__layout.addWidget(label, i, 0)
        label = QLabel('Color: ', self)
        self.__textLabels.append(label)
        self.__layout.addWidget(label, 3, 0)

    def __initializeColorLabels(self) :
        for i in self._components + (len(self._components), ) :
            label = QLabel(self)
            self.__colorLabels.append(label)
            self.__layout.addWidget(label, i, 2)
        

    def __init__(self, parent) :
        super(AbstractColorIntervalWidget, self).__init__(parent)
        self._widgetSize = [ [200, 600], [150, 150] ]    #[ [minWidth, maxWidth], [minHeight, maxHeight]]
        self.__layout = None
        self.__textLabels = []
        self.__sliders = []
        self.__colorLabels = []
        self.__constructQWidgets()
        self.setMinimumSize(self._widgetSize[0][0], self._widgetSize[1][0])
        self.setMaximumSize(self._widgetSize[0][1], self._widgetSize[1][1])

    def invert(self, color) :
        inverted = QColor()
        inverted.setRed(255 - color.red());
        inverted.setGreen(255 - color.green());
        inverted.setBlue(255 - color.blue());
        return inverted;

    def _valueChangedSlot(self, i, val) :
        print('WARNING: Pure virtual method AbstractColorIntervalWidget::_valueChangedSlot() has been called')
        pass

    def _redrawColorLabel(self, labelIndex, lc, uc, lValue, uValue) :
        if labelIndex >= len(self.__colorLabels) :
            return
        label = self.__colorLabels[labelIndex]
        pixmap = QPixmap(101, 26)
        painter = QPainter(pixmap)
        lowerColorRect = QRect(0, 0, 50, 25)
        upperColorRect = QRect(50, 0, 50, 25)

        font = QFont('Times', 11)
        painter.setFont(font)

        painter.setPen(Qt.black);
        painter.setBrush(lc);
        painter.drawRect(lowerColorRect);
        painter.setPen(self.invert(lc));
        painter.drawText(lowerColorRect.translated(8, 2), 0, str(lValue));

        painter.setPen(Qt.black);
        painter.setBrush(uc);
        painter.drawRect(upperColorRect);
        painter.setPen(self.invert(uc));
        painter.drawText(upperColorRect.translated(8, 2), 0, str(uValue));
        del painter

        label.setPixmap(pixmap);


    def component(self, c) :
        if c in self._components:
            return ( self.__sliders[c].lowerValue(), self.__sliders[c].upperValue() )
        else :
            return None
        
    def qLower(self) :
        print('WARNING: Pure virtual method AbstractColorIntervalWidget::qLower() has been called')
        pass
    def qUpper(self) :
        print('WARNING: Pure virtual method AbstractColorIntervalWidget::qUpper() has been called')
        pass

    def npLower(self) :
        color = list()
        for i in self._components :
            color.append(self.__sliders[i].lowerValue())
        return numpy.array(color, dtype = 'uint8')

    def npUpper(self) :
        color = list()
        for i in self._components :
            color.append(self.__sliders[i].upperValue())
        return numpy.array(color, dtype = 'uint8')

    def destroy(self) :
        for i in self._components :
            self.__sliders[i].hide()
            self.__sliders[i].deleteLater()
        for i in self._components + (3,):
            self.__textLabels[i].hide()
            self.__textLabels[i].deleteLater()
            self.__colorLabels[i].hide()
            self.__colorLabels[i].deleteLater()


