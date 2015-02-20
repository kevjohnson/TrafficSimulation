class Node(object):
	def __init__(self, data):
		self.data = data
		self.next = None

class FIFO(object):
    def __init__(self):
    	self.length = 0
    	self.head = None
    	self.tail = None

    def is_empty(self):
    	return (self.length == 0)

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
def test():
	ls = [1, 'good', 'creative']
	ls1 = [2, 'better', 'haha']
	s = FIFO()
	s.insert(ls)
	s.insert(ls1)
	if s.is_empty() == False:
		print s.remove()
test()