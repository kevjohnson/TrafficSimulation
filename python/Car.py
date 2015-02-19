class Car(object):

    """This class represents a car"""

    def __init__(self, origin, destination, route, entryTime):
        self.origin = origin
        self.destination = destination
        self.route = route
        self.entryTime = entryTime

    def getOrigin(self):
        return self.origin

    def setOrigin(self, origin):
        self.origin = origin

    def getDestination(self):
        return self.destination

    def setDestination(self, destination):
        self.destination = destination

    def getEntryTime(self):
        return self.entryTime

    def setEntryTime(self, entryTime):
        self.entryTime = entryTime

    def getNextLane(self):
        return self.route.pop(0)

    def getNextLaneNoRemove(self):
        return self.route[0]

    def getRoute(self):
        return self.route
