class Light(object):

    """This class stores the state of a light."""

    def __init__(self, signalTiming):
        self.state = 0
        self.signalTiming = signalTiming

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def changeState(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

    def getNextChange(self):
        if self.state == 0:
            return self.signalTiming[1]
        else:
            return self.signalTiming[0]
