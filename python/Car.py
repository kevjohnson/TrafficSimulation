class Car(object):

    """This class represents a car"""

    def __init__(self, origin, entryTime, redLight):
        self.origin = origin
        self.entryTime = entryTime
        self.redLight = redLight

    def getOrigin(self):
        return self.origin

    def setOrigin(self, origin):
        self.origin = origin

    def getEntryTime(self):
        return self.entryTime

    def setEntryTime(self, entryTime):
        self.entryTime = entryTime

    def addRedLight(self, time):
        self.redLight += time
