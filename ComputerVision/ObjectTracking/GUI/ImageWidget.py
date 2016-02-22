from PyQt5.QtCore import QTimer, QPoint, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
import QtCV
import cv2
import numpy

class ImageWidget(QLabel):
    """Prints image in cv::Mat format and handles mouse events"""
    contourChanged = pyqtSignal(list)
    def __init__(self, qtParent = None) :
        super(QLabel, self).__init__(qtParent, )
        self.setText('Loading...')
        self._showContour = False
        

    def setCvImage(self, image) :
        self.originalHeight, self.originalWidth, _ = image.shape
        if self._showContour == True :
            cnt = numpy.array(self._contour, dtype=numpy.int32)
            cv2.drawContours(image, [cnt], 0, [255, 255, 255], 3)
        self.qtPixmap = QtCV.cvMatToQPixmap(image);
        self.qtPixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        self.setPixmap(self.qtPixmap)

    def widthZoom(self) :
        return self.qtPixmap.width() / self.originalWidth

    def heightZoom(self) :
        return self.qtPixmap.height() / self.originalHeight


    #===========  Mouse events  =================
    def mousePressEvent(self, mouseEvent):
        pos = mouseEvent.pos()
        x = pos.x() / self.widthZoom()
        y = pos.y() / self.heightZoom()
        self._contour = [(x, y)]
        self._showContour = True

    def mouseMoveEvent(self, mouseEvent):
        pos = mouseEvent.pos()
        x = pos.x() / self.widthZoom()
        y = pos.y() / self.heightZoom()
        self._contour.append((x, y))

    def mouseReleseEvent(self, mouseEvent):
        self._showContour = False
        self.contourChanged.emit(self._contour)



