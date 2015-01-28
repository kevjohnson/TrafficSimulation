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
        for i in [1, 4, 5, 8, 9, 12, 13, 15, 19]:
            self.lights[i - 1].setState(1)
        self.lanes = [Lane.Lane(self.capacity[i], self.lights[i])
                      for i in range(19)]
        self.arrivalLanes = [1, 2, 3, 6, 7, 10, 11, 14, 17, 18, 19]
        for i in self.arrivalLanes:
            self.eventList.put(
                (round(-math.log(random.random()) / self.rate[i - 1]),
                    i, "arrival"))
        for i in range(0, 30000, 15):
            for j in range(19):
                self.eventList.put((i, j, "light change"))
        self.nextLanes = {
            1: (5, 99, 99),
            2: (99, 5, 99),
            3: (99, 99, 5),
            4: (99, 99, 99),
            5: (9, 99, 99),
            6: (99, 9, 4),
            7: (99, 4, 9),
            8: (4, 99, 99),
            9: (13, 99, 99),
            10: (99, 13, 8),
            11: (99, 8, 13),
            12: (8, 99, 99),
            13: (16, 99, 99),
            14: (99, 12, 16),
            15: (12, 99, 99),
            16: (99, 99, 99),
            17: (99, 99, 15),
            18: (99, 15, 99),
            19: (15, 99, 99)
        }

    def nextEvent(self):
        event = self.eventList.get()
        print(event)
        self.time += event[0]
        if event[2] == "arrival":
            car = Car.Car(origin=event[1], entryTime=self.time)
            self.lanes[event[1]].addCar(car)
            self.eventList.put(
                (self.time + round(-math.log(random.random()) /
                                   self.rate[event[1]]),
                 event[1], "arrival"))
        else:
            for i in range(19):
                self.lights[i].changeState()
        self.updateSimulation()
        return self.time

    def updateSimulation(self):
        nextEvent = self.eventList.get()
        timeUntilNextEvent = nextEvent[1] - self.time
        self.eventList.put(nextEvent)
        numCars = math.floor(self.flow * (timeUntilNextEvent - self.time))
        updateOrder = [16, 13, 9, 5, 1, 4, 8, 12, 15, 19, 2, 3, 6, 7,
                       10, 11, 14, 17, 18]
        for i in updateOrder:
            for j in range(max(numCars, self.lanes[i-1].getCars().qsize())):
                car = self.lanes[i].getNextCar()
                r = random.random()
                if r < self.turnProbs[0]:
                    self.moveCar(car, self.nextLanes[i][0],
                                 i, self.time + j / self.flow)
                elif r < self.turnProbs[1]:
                    self.moveCar(car, self.nextLanes[i][1],
                                 i, self.time + j / self.flow)
                else:
                    self.moveCar(car, self.nextLanes[i][2],
                                 i, self.time + j / self.flow)

    def moveCar(self, car, nextLane, currentLane, time):
        if nextLane == 99:
            self.writer.writerow(
                [car.getOrigin(), currentLane, time - car.getEntryTime()])
        else:
            self.lanes[nextLane].addCar()
