from enum import Enum
#from math import abs

class Move (Enum) :
    No = 0
    Up = 1
    Right = 2
    Down = 4
    Left = 8
    Forward = 16
    Back = 32


class ObjectTracker :
    lastX = None
    lastY = None
    lastR = None
    epsilon = 80
    r_epsilon = 250
    moveTo = Move.No

    def __init__(self, x, y, r) :
        self.setNewPosition(x, y, r)

    def position(self) :
        return ( self.lastX, self.lastY, self.lastR )

    def setNewPosition(self, x, y, r = None) :
        self.lastX = x
        self.lastY = y
        if r is None :
            return
        self.lastR = r

    def processNewPositions(self, objects) :
        for x,y,r in objects :
            if abs(x - self.lastX) > self.epsilon :
                continue
            if abs(y - self.lastY) > self.epsilon :
                continue
            #if abs(r - self.lastR) > self.r_epsilon :
                #continue
            #WARNING может работать неправильно, если рядом будет другой объект
            if self.lastX < x :
                self.moveTo = self.moveTo or Move.Right
            elif x < self.lastX :
                self.moveTo = self.moveTo or Move.Left

            if self.lastY < y :
                self.moveTo = self.moveTo or Move.Up
            elif y < self.lastY :
                self.moveTo = self.moveTo or Move.Down

            if self.lastR < r :
                self.moveTo = self.moveTo or Move.Forward
            elif r < self.lastR :
                self.moveTo = self.moveTo or Move.Back

            self.setNewPosition(x, y, r)








