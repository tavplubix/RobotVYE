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


class SimpleObjectTracker :
    def __init__(self, x, y, r) :
        self.lastX = None
        self.lastY = None
        self.lastR = None
        self.epsilon = 80
        self.r_epsilon = 250
        self.moveTo = Move.No
        self.setTrackingObject(x, y, r)

    def objectPosition(self) :
        if self.lastX is None or self.lastY is None or self.lastR is None :
            return (0, 0, 0)
        else :
            return ( self.lastX, self.lastY, self.lastR )

    def setTrackingObject(self, x = None, y = None, r = None) :
        self.lastX = x
        self.lastY = y
        self.lastR = r



    def processNewPositions(self, objects) :
        for x,y,r in objects :
            if abs(x - self.lastX) > self.epsilon :
                continue
            if abs(y - self.lastY) > self.epsilon :
                continue
            #if abs(r - self.lastR) > self.r_epsilon :
                #continue
            #WARNING ????? ???????? ???????????, ???? ????? ????? ?????? ??????
            self.moveTo = Move.No
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

            self.setTrackingObject(x, y, r)








