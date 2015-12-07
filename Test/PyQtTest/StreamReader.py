import cv2
from PyQt5.QtWidgets import QErrorMessage

class CannotReadFrame :
    pass

class StreamReader :
    def __init__(self) :
        #заглушка
        qem = QErrorMessage()
        qem.showMessage('Не удаётся подключиться к Raspberry Pi: Будет подключена локальная камера')
        qem.exec()
        self.__capturedDevice = cv2.VideoCapture(0)    

    def __del__(self) :
        if self.__capturedDevice is None :
            return
        self.__capturedDevice.release()

    def getFrame(self) :
        if self.__capturedDevice is None :
            raise CannotReadFrame
        retVal, frame = self.__capturedDevice.read()
        if retVal == False :
            raise CannotReadFrame
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #return cv2.resize(frame, (0, 0), fx = 1.6, fy = 1.6)

    def readable(self) :
        #заглушка
        return True




