from genome import Genome

class Node( object ):

	def __init__( self, val=None):

class Tree( object ):

	def __init__(self, genome, connections=None): 
		self.genome = genome
		if connections is not None:
			self.connections = connections
		else:
			self.connections = []

	def __iter__(self):
		return iter(self.connections)

	def addConnection(self, otherTree ):
		self.connections.append(otherTree)
		otherTree.connections.append(self)

	def isLeaf(self):
		return len(self.connections) in [0,1]




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

	# Factory Method
	def parseTuple( tup ):
		for el in tup:


def test():
	a = Genome(name="a")
	aT = Tree( a )
	b = Genome(name="b")
	bT = Tree(b )
	c = Genome(name="c")
	cT = Tree(c)
	d = Genome(name="d")
	e = Genome(name="e")
	f = Genome(name="f")

	print(aT)
	print(bT)
	aT.addConnection( bT)
	print(aT)
	aT.addConnection( cT)
	print(aT)

if __name__ == "__main__":
	test()

	
