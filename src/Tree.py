


class Tree( object ):

	def __init__(self, genome, connections=[]): 
		self.genome = genome
		self.connections = connections

	def __iter__(self):
		return iter(self.connections)

	def addConnection(self, node ):
		self.connections.append(node)
		node.addConnection(self)

	def isLeaf(self):
		return len(self.connections) == 1

	def __str__(self):
		if self.isLeaf():
			return self.genome.name()
		else:
			out = "("
			for subtree in self:
				out += str(subtree) + ","
			out += ")"

	def size(self):
		if self.isLeaf():
			return 1
		else:
			size = 0
			for subtree in self:
				size += subtree.size()
			return size

	def populateTips(self, tips):
		if self.isLeaf():
			tips.append( (self.genome, self))
		else:
			self.populateTips( tips )

	
