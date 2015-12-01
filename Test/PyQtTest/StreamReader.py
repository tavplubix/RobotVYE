import cv2
from PyQt5.QtWidgets import QErrorMessage

class CannotReadFrame :
    pass

class StreamReader :
    _capturedDevice = None
    def __init__(self) :
        #заглушка
        qem = QErrorMessage()
        qem.showMessage('Не удаётся подключиться к Raspberry Pi: Будет подключена локальная камера')
        qem.exec()
        self._capturedDevice = cv2.VideoCapture(0)    

    def __del__(self) :
        if self._capturedDevice is None :
            return
        self._capturedDevice.release()

    def getFrame(self) :
        if self._capturedDevice is None :
            raise CannotReadFrame
        retVal, frame = self._capturedDevice.read()
        if retVal == False :
            raise CannotReadFrame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return cv2.resize(frame, (0, 0), fx = 1.6, fy = 1.6)

    def readable(self) :
        #заглушка
        return True




