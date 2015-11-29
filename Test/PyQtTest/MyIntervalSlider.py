from enum import Enum
from PyQt5.QtCore import QDir, QRect, Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtWidgets import QStyle, QStyleFactory, QStyleOptionSlider, QStylePainter
from PyQt5.QtWidgets import QWidget, QAbstractSlider


#==================================================================================================
#					MyIntervalSliderOptions Implementation
#==================================================================================================

class MyIntervalSliderOptions :
    _slider = None
    _lowerValue = 0
    _upperValue = 255
    def __init__(self, slider) :
        self._lowerValue = slider.minimum();
        self._upperValue = slider.maximum();
        self._slider = slider
    
    def copyOptions(self) :
        opt = QStyleOptionSlider()
        opt.initFrom(self._slider)
        opt.maximum = self._slider.maximum();
        opt.minimum = self._slider.minimum();
        opt.orientation = self._slider.orientation()
        opt.pageStep = self._slider.pageStep()
        opt.singleStep = self._slider.singleStep()
        return opt

    def getCommonOptions(self) :
        return self.copyOptions();
    
    def getLowerHandleOptions(self) :
        opt = self.copyOptions()
        opt.subControls = QStyle.SC_SliderHandle;
        opt.sliderPosition = self._lowerValue;
        opt.sliderValue = self._lowerValue;
        return opt;
    
    def getUpperHandleOptions(self) :
        opt = self.copyOptions()
        opt.subControls = QStyle.SC_SliderHandle;
        opt.sliderPosition = self._upperValue;
        opt.sliderValue = self._upperValue;
        return opt;
    
    def getGrooveOptions(self) :
        opt = self.copyOptions()
        opt.subControls = QStyle.SC_SliderGroove or QStyle.SC_SliderTickmarks;
        return opt;
    
    def setLowerValue(self, value) :
        if value >= self._upperValue :
            return False;
        self._lowerValue = value;
        self._lowerPosition = value;
        return True;
    
    def setUpperValue(self, value) :
        if value <= self._lowerValue :
            return False;
        self._upperValue = value;
        self._upperPosition = value;
        return True;

    def lowerValue(self) :
        return self._lowerValue

    def upperValue(self) :
        return self._upperValue
	#int lowerValue() const { return m_lowerValue; };
	#int upperValue() const { return m_upperValue; };


class SubControl(Enum) :
    No = 0
    Groove = QStyle.SC_SliderGroove
    LowerHandle = QStyle.SC_SliderHandle
    Tickmarks = QStyle.SC_SliderTickmarks
    UpperHandle = 0x08


#==================================================================================================
#					MyIntervalSlider Implementation
#==================================================================================================


class MyIntervalSlider(QAbstractSlider) :
    upperValueChanged = pyqtSignal(int)
    lowerValueChanged = pyqtSignal(int)
    _style = QStyleFactory.create("Fusion");
    _options = None
    _activeSubControl = SubControl.No
    def __init__(self, parent) :
        super(MyIntervalSlider, self).__init__(parent)
        self.setStyle(self._style)
        self._options = MyIntervalSliderOptions(self)
        self.setAcceptDrops(True)
        self.setMinimumWidth(255)

    def __init__(self) :
        super(MyIntervalSlider, self).__init__()
        self.setStyle(self._style)
        self._options = MyIntervalSliderOptions(self)
        self.setAcceptDrops(True)
        self.setMinimumWidth(255)

    def paintEvent(self, paintEvent):
       painter = QStylePainter(self)
       painter.drawComplexControl(QStyle.CC_Slider, self._options.getGrooveOptions())
       painter.drawComplexControl(QStyle.CC_Slider, self._options.getLowerHandleOptions())
       painter.drawComplexControl(QStyle.CC_Slider, self._options.getUpperHandleOptions())

    def subcontrolOnPosition(self, position) :
        element = QStyle.SubControl()
        rect = QRect()
        rect = self._style.subControlRect(QStyle.CC_Slider, self._options.getUpperHandleOptions(), QStyle.SC_SliderHandle);
        if rect.contains(position) :
            return SubControl.UpperHandle;
        rect = self._style.subControlRect(QStyle.CC_Slider, self._options.getLowerHandleOptions(), QStyle.SC_SliderHandle);
        if rect.contains(position) :
            return SubControl.LowerHandle;
        rect = self._style.subControlRect(QStyle.CC_Slider, self._options.getGrooveOptions(), QStyle.SC_SliderGroove);
        if rect.contains(position) :
            return SubControl.Groove;
        return SubControl.No;

    def mousePressEvent(self, event) :
        pos = event.pos()
        if event.button() == Qt.LeftButton :
            self._activeSubControl = self.subcontrolOnPosition(pos);
            self.clearFocus();
        event.accept();

    def mouseMoveEvent(self, event) :
        pos = event.pos()
        min = self._options.getCommonOptions().minimum;
        max = self._options.getCommonOptions().maximum;
        pixelsPerOne = float(self.width()) / float(self.maximum() - self.minimum());
        ones = float(pos.x()) / pixelsPerOne;
        newValue = min + int(ones);
        if newValue < min :
            newValue = min;
        if newValue > max :
            newValue = max;

        if self._activeSubControl == SubControl.LowerHandle :
            self._options.setLowerValue(newValue);
            self.lowerValueChanged.emit(self._options.lowerValue());

        if self._activeSubControl == SubControl.UpperHandle :
            self._options.setUpperValue(newValue);
            self.upperValueChanged.emit(self._options.upperValue());

        self.valueChanged.emit(newValue);
        event.accept();
        self.update();

    def mouseReleaseEvent(self, event) :
        if event.button() == Qt.LeftButton :
            self.activeSubControl = SubControl.No
        event.accept()

    def setUpperValue(self, value) :
        oldValue = self._options.upperValue();
        self._options.setUpperValue(value);
        if value != oldValue :
            self.upperValueChanged.emit(self._options.upperValue());
            self.valueChanged.emit(self._options.upperValue());

    def setLowerValue(self, value) :
        oldValue = self._options.lowerValue();
        self._options.setLowerValue(value);
        if value != oldValue :
            self.lowerValueChanged.emit(self._options.lowerValue());
            self.valueChanged.emit(self._options.lowerValue());


