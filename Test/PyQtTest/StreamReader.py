import cv2
from PyQt5.QtWidgets import QErrorMessage
#from socket import socket
#from pickle import loads
from Socket import Socket

class CannotReadFrame :
    pass

class StreamReader :
    def __init__(self) :
        self._server = None
        self._capturedDevice = None
        pass

    def connect(self, addr = '127.0.0.1', port = 4242) :
        try:
            self._server = Socket()
            statusCode = self._server.connect_ex((addr, port))
            if statusCode != 0 :
                raise statusCode
        except :
            self.connectLocalCamera()

    def connectLocalCamera(self) :
        self.close()
        qem = QErrorMessage()
        qem.showMessage('Не удаётся подключиться к Raspberry Pi: Будет подключена локальная камера')
        qem.exec()
        self.__capturedDevice = cv2.VideoCapture(0)    

    def __del__(self) :
        self.close()

    def getFrame(self) :
        if self._server is not None :
            try: 
                return self._getFrameFromRemoteCamera() 
            except: 
                self.connectLocalCamera()

        if self._capturedDevice is not None :
            try: 
                return self._getFrameFromLocalCamera() 
            except: 
            raise CannotReadFrame


    def _getFrameFromRemoteCamera(self) :
        self._server.sendObject('get_frame')
        frame = self._server.recvObject()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def _getFrameFromLocalCamera(self) :
        retVal, frame = self._capturedDevice.read()
        if retVal == False :
            raise CannotReadFrame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame#cv2.resize(frame, (0, 0), fx = 1.6, fy = 1.6)

    def readable(self) :
        #заглушка
        return True

    def recvall(self, sock, size) :
        binary = sock.recv(size)
        diff = size - len(binary)
        while diff :
            buf = sock.recv(diff)
            diff = diff - len(buf)
            binary = binary + buf
        return binary

    def close(self) :
        if self._capturedDevice is not None :
            self._capturedDevice.release()
            self._capturedDevice = None
        if self._server is not None :
            try:
                #self._server.sendObject('close_conection')
                self._server.sendObject('exit')
                self._server.close()
            except:
                pass
            finally:
                self._server = None



