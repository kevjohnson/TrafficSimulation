import queue
import Lane
import Light
import Car
import random
import math
import csv


class TrafficSimulation(object):

    """This class governs the entire simulation"""

    def __init__(self, rate, capacity, flow, turnProbs, outFile):
        self.writer = csv.writer(outFile)
        self.rate = rate
        self.flow = flow
        self.capacity = capacity
        self.time = 0
        self.eventList = queue.PriorityQueue()
        self.turnProbs = turnProbs
        self.lights = [Light.Light() for i in range(19)]
        for i in [0, 3, 4, 7, 8, 11, 12, 14, 18]:
            self.lights[i - 1].setState(1)
        self.lanes = [Lane.Lane(self.capacity[i], self.lights[i])
                      for i in range(19)]
        self.arrivalLanes = [0, 1, 2, 5, 6, 9, 10, 13, 16, 17, 18]
        for i in self.arrivalLanes:
            self.eventList.put(
                (-math.log(random.random()) / self.rate[i],
                    i, "arrival"))
        for i in range(15, 30000, 15):
            for j in range(19):
                self.eventList.put((i, j, "light change"))
        self.nextLanes = {
            0: (4, 99, 99),
            1: (99, 4, 99),
            2: (99, 99, 4),
            3: (99, 99, 99),
            4: (8, 99, 99),
            5: (99, 8, 3),
            6: (99, 3, 8),
            7: (3, 99, 99),
            8: (12, 99, 99),
            9: (99, 12, 7),
            10: (99, 7, 12),
            11: (7, 99, 99),
            12: (15, 99, 99),
            13: (99, 11, 16),
            14: (11, 99, 99),
            15: (99, 99, 99),
            16: (99, 99, 14),
            17: (99, 14, 99),
            18: (14, 99, 99)
        }

    def nextEvent(self):
        event = self.eventList.get()
        self.time = event[0]
        l = event[1]
        if event[2] == "arrival":
            car = Car.Car(origin=l, entryTime=self.time)
            if (self.lanes[l].getCars().empty() == True and
                    self.lights[l].getState() == 1):
                self.eventList.put(
                    (self.time + self.flow, l, "move car"))
            self.lanes[l].addCar(car)
            self.eventList.put(
                (self.time + (-math.log(random.random()) /
                              self.rate[l]),
                 l, "arrival"))
        elif event[2] == "move car":
            if (self.lights[l].getState() == 1 and
                    self.lanes[l].getCars().empty() is not True):
                r = random.random()
                if r < self.turnProbs[0]:
                    nextLane = self.nextLanes[l][0]
                elif r < (self.turnProbs[0] + self.turnProbs[1]):
                    nextLane = self.nextLanes[l][1]
                else:
                    nextLane = self.nextLanes[l][2]
                if nextLane == 99:
                    car = self.lanes[l].getNextCar()
                    self.writer.writerow([car.getOrigin(), l,
                                          self.time - car.getEntryTime()])
                elif self.lanes[nextLane].getCars().full() is not True:
                    car = self.lanes[l].getNextCar()
                    self.lanes[nextLane].addCar(car)
                if self.lanes[l].getCars().empty() is not True:
                    self.eventList.put(
                        (self.time + self.flow, l, "move car"))
        else:
            self.lights[l].changeState()
            if (self.lights[l].getState() == 1 and
                    self.lanes[l].getCars().empty() is not True):
                self.eventList.put(
                    (self.time + self.flow, l, "move car"))
        return self.time
