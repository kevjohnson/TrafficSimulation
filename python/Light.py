class Light(object):

    """This class stores the state of a light."""

    def __init__(self):
        self.state = 0

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
