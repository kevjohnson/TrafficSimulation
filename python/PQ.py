
class PriorQ(object):
	def __init__(self):
		self.items = []
	
	def is_empty(self):
		return self.items == []

	def insert(self, item):
		self.items.append(item)

	def remove(self):
		mini = 0
		for i in range(1, len(self.items)):
			if self.items[i] < self.items[mini]: mini = i
		item = self.items[mini]
		self.items.pop(mini)
		return item


def test():
	pq = PriorQ()
	
	pq.insert([6, 'better', 'best'])
	pq.insert([5, 'good', 'better'])
	while not pq.is_empty():
		print pq.remove()
test()