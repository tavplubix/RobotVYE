from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import numpy
import cv2


def cvMatToQImage(cvmat) :
    if cvmat is None :
        return QImage()
    
    if cvmat.dtype == numpy.uint8 :
        if len(cvmat.shape) == 2:
            temp = cv2.cvtColor(cvmat, cv2.COLOR_GRAY2RGB)

        elif len(cvmat.shape) == 3:
            if cvmat.shape[2] == 3:
                #temp = cvmat;
                temp = cv2.cvtColor(cvmat, cv2.COLOR_BGR2RGB)
        qimage = QImage(temp.data, temp.shape[1], temp.shape[0], temp.strides[0], QImage.Format_RGB888);
        return qimage.copy()
    return False;

def cvMatToQPixmap(cvmat) :
    return QPixmap(cvMatToQImage(cvmat))

def qImageToCvMat(qim) :
    incomingImage = qim.convertToFormat(4)
    width = qim.width()
    height = qim.height()

    ptr = qim.bits()
    ptr.setsize(qim.byteCount())
    cvmat = numpy.array(ptr).reshape(height, width, 4)
    return cvmat

def qPixmapToCvMat(qpm) :
    return qImageToCvMat(QImage(qpm))


