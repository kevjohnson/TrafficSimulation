import Queue
import Lane
import Light
import Car


class TrafficSimulation(object):

    """This class governs the entire simulation"""

    def __init__(self, rate, capacity, flow):
        super(TrafficSimulation, self).__init__()
        self.rate = rate
        self.capacity = capacity
        self.flow = flow
        self.counter = 0
        self.eventList = Queue.PriorityQueue()
        self.lanes = []
