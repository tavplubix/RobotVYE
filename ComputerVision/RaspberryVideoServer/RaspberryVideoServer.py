#from time import time
import cv2
import threading
import logging
logging.basicConfig(level = logging.DEBUG)
from Socket import Socket

stopped = False

def processConnection(client, camera) :
    global stopped
    clientaddr = str(client.getpeername())
    logging.debug('New client connected: addr=' + clientaddr)
    while True :
        request = client.recvObject()
        if request == 'get_frame' :
            retVal, frame = camera.read()
            client.sendObject(frame)
        elif request == 'close_conection' :
            client.close()
            break
        elif request == 'exit' :
            logging.info('Video server will be stopped ("exit" message got)')
            client.close()
            stopped = True
            break
        else :
            logging.warning('Unknown request method "' + request + '" : connection closed')
            client.close()
            break
    logging.debug('Conection with client closed: addr=' + clientaddr)
    exit(0)



logging.info('Video server has been started')

server = Socket()
server.bind(('127.0.0.1', 4242))
server.listen(5)

camera = cv2.VideoCapture(0)


while not stopped:
    connection = server.tryaccept(3)
    if connection is None :
        continue
    client,addr = connection
    thread = threading.Thread(target=processConnection, args=(client, camera))
    thread.start()

#for thread in threading.enumerate() :
#    if thread != threading.currentThread() :
#        thread.join()

logging.info('Video server has been stopped')

quit()