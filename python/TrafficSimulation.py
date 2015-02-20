import queue
import Lane
import Light
import Car
import random
import math


class TrafficSimulation(object):

    """This class governs the entire simulation"""

    def __init__(self, arrivalRates, travelMatrix, capacity, flow,
                 signalTimings, timeLimit, synchronous, seed):
        random.seed(seed)
        self.output = []
        self.carsInSystem = 0
        self.id = 0
        self.finished = False
        self.timeLimit = timeLimit
        self.arrivalRates = arrivalRates
        self.signalTimings = signalTimings
        self.flow = flow
        self.capacity = capacity
        self.time = 0
        self.eventList = queue.PriorityQueue()
        self.travelMatrix = travelMatrix
        self.lights = [Light.Light(self.signalTimings[i]) for i in range(19)]
        if synchronous:
            for i in [0, 3, 4, 7, 8, 11, 12, 13, 14, 18]:
                self.lights[i].setState(1)
        else:
            for i in [1, 2, 4, 7, 9, 10, 12, 13, 14, 18]:
                self.lights[i].setState(1)
        self.lanes = [Lane.Lane(self.capacity[i], self.lights[i])
                      for i in range(19)]
        for lane in self.arrivalRates:
            self.scheduler(-math.log(random.random()) /
                           self.arrivalRates[lane], "System Arrival", lane)
        for i in range(19):
            self.scheduler(self.lights[i].getNextChange(), "Light Change", i)
        self.intersections = {0: (0, 1, 2, 3),
                              1: (4, 5, 6, 7),
                              2: (8, 9, 10, 11),
                              3: (12, 99, 13, 14),
                              4: (15, 16, 17, 18)}

    def run(self):
        while self.finished is False:
            event = self.eventList.get()
            self.time = event[0]
            self.eventHandler(event)
            print("{:.2%}".format(self.time / self.timeLimit), end="\r")
            if self.time > self.timeLimit:
                self.finished = True

    def eventHandler(self, event):
        if event[2] == "System Arrival":
            self.systemArrival(event[3])
        elif event[2] == "Lane Departure":
            self.laneDeparture(event[3])
        elif event[2] == "Lane Arrival":
            self.laneArrival(event[3])
        elif event[2] == "Lane Full":
            self.laneFull(event[3])
        else:
            self.signalChange(event[3])

    def scheduler(self, timestamp, eventType, eventData):
        self.eventList.put((timestamp, self.id, eventType, eventData))
        self.id += 1

    def systemArrival(self, eventData):
        lane = eventData
        self.scheduler(self.time - math.log(random.random()) /
                       self.arrivalRates[lane], "System Arrival", lane)
        destination = self.getDestination(lane)
        route = self.getRoute(lane, destination)
        car = Car.Car(origin=lane, destination=destination,
                      route=route, entryTime=self.time)
        if car.getOrigin() != car.getDestination():
            self.scheduler(self.time + self.flow, "Lane Arrival",
                           (lane, car))

    def laneDeparture(self, eventData):
        lane = eventData
        if (self.lights[lane].getState() == 1 and
                self.lanes[lane].getCars().empty() is not True):
            car = self.lanes[lane].getNextCar()
            nextLane = car.getNextLane()
            if nextLane not in (3, 4, 7, 8, 11, 12, 14, 15):
                self.output.append((self.time, car.getOrigin(),
                                    car.getDestination(),
                                    self.time - car.getEntryTime()))
                self.scheduler(self.time + self.flow, "Lane Departure", lane)
            elif self.lanes[nextLane].getCars().full() is True:
                self.scheduler(self.time + self.flow, "Lane Full",
                               (lane, nextLane, car))
            else:
                self.scheduler(self.time + self.flow, "Lane Arrival",
                               (nextLane, car))
                self.scheduler(self.time + self.flow, "Lane Departure", lane)

    def laneFull(self, eventData):
        lane = eventData[0]
        nextLane = eventData[1]
        car = eventData[2]
        if self.lanes[nextLane].getCars().full() is True:
            self.scheduler(self.time + self.flow, "Lane Full",
                           (lane, nextLane, car))
        else:
            self.scheduler(self.time + self.flow, "Lane Arrival",
                           (nextLane, car))
            self.scheduler(self.time + self.flow, "Lane Departure", lane)

    def laneArrival(self, eventData):
        lane = eventData[0]
        car = eventData[1]
        if self.lanes[lane].getCars().full() is True:
            self.scheduler(self.time + self.flow, "Lane Arrival",
                           (lane, car))
        elif self.lanes[lane].getCars().empty() is True:
            self.lanes[lane].addCar(car)
            self.scheduler(self.time + self.flow, "Lane Departure", lane)
        else:
            self.lanes[lane].addCar(car)

    def signalChange(self, eventData):
        light = eventData
        self.lights[light].changeState()
        if (self.lights[light].getState() == 1 and
                self.lanes[light].getCars().empty() is not True):
            self.scheduler(self.time + self.flow, "Lane Departure", light)
        self.scheduler(self.time + self.lights[light].getNextChange(),
                       "Signal Change", light)

    def getDestination(self, origin):
        r = random.random()
        row = self.travelMatrix[origin]
        destinationIndex = [i for i, v in enumerate(row) if r < v][0]
        destination = list(self.arrivalRates.keys())[destinationIndex]
        return destination

    def getRoute(self, origin, destination):
        originIntersection = [k for k, v in self.intersections.items()
                              if origin in v][0]
        destinationIntersection = [k for k, v in self.intersections.items()
                                   if destination in v][0]
        routeFinished = False
        route = []
        currentIntersection = originIntersection
        if originIntersection > destinationIntersection:
            while routeFinished is not True:
                route.append(self.intersections[currentIntersection - 1][3])
                currentIntersection = currentIntersection - 1
                if (route[len(route) - 1] in
                        self.intersections[destinationIntersection]):
                    route.append(destination)
                    routeFinished = True
        elif originIntersection < destinationIntersection:
            while routeFinished is not True:
                route.append(self.intersections[currentIntersection + 1][0])
                currentIntersection = currentIntersection + 1
                if (route[len(route) - 1] in
                        self.intersections[destinationIntersection]):
                    route.append(destination)
                    routeFinished = True
        else:
            route.append(destination)
        return route

    def getOutput(self):
        return self.output
