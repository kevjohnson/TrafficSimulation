class Node(object):

    def __init__(self, data):
        self.data = data
        self.next = None


class FIFO(object):

    def __init__(self, capacity):
        self.length = 0
        self.head = None
        self.tail = None
        self.capacity = capacity

    def is_empty(self):
        return (self.length == 0)

    def is_full(self):
        return (self.length >= self.capacity)

    def __iter__(self):
        return self

    def insert(self, item):
        node = Node(item)
        node.next = None
        if self.length == 0:
            self.head = self.tail = node
        else:
            tail = self.tail
            tail.next = node
            self.tail = node
        self.length = self.length + 1

    def remove(self):
        item = self.head.data
        self.head = self.head.next
        self.length = self.length - 1
        if self.length == 0:
            self.last = None
        return item
