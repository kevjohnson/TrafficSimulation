import Queue


class Lane(object):

    """This class stores all the information we need for each lane"""

    def __init__(self, capacity, light, nextLanes):
        self.capacity = capacity
        self.light = light
        self.nextLanes = nextLanes
        self.cars = Queue.Queue(maxsize=capacity)

    def getCapacity(self):
        return self.capacity

    def setCapacity(self, capacity):
        self.capacity = capacity

    def getLight(self):
        return self.light

    def setLight(self, light):
        self.light = light

    def addCar(self, car):
        self.cars.put(car)

    def getNextCar(self):
        return self.cars.get()
