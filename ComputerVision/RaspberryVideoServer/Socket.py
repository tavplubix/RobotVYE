from socket import socket
from socket import timeout as TimeoutException
import pickle




class Socket() :

    def __init__(self, sock = socket()) :
        self._sock = sock

    def __getattr__(self, attr) :
        return self._sock.__getattribute__(attr)

    def sendObject(self, object) :
        binaryData = pickle.dumps(object)
        intSize = len(binaryData)
        binSize = intSize.to_bytes(8, 'big')
        #send 8 bytes of message lenght first
        self.send(binSize)     
        #the send intSize bytes of data
        self.send(binaryData)       

    def _recvall(self, size) :
        binary = self.recv(size)
        diff = size - len(binary)
        while diff :
            buf = self.recv(diff)
            diff = diff - len(buf)
            binary = binary + buf
        return binary

    def recvObject(self) :
        #get 8 bytes of message lenght first
        binSize = self._recvall(8)     
        intSize = int.from_bytes(binSize, 'big')
        #then get intSize bytes of data
        binaryData = self._recvall(intSize)
        #and then return serialized data
        return pickle.loads(binaryData)

    def accept(self) :
        sock,addr = self._sock.accept()
        return (Socket(sock), addr)

    def tryaccept(self, timeout = 0) :
        if self.timeout != self._sock.gettimeout() :
            self._sock.settimeout(timeout)
        try :
            sock,addr = self._sock.accept()
        except TimeoutException as e :
            return None
        else :
            return (Socket(sock), addr)

