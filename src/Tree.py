from genome import Genome
from PyGrimmInterface import GrimmInterface as Grimm
from random import randint

class Tree( object ):

	def __init__(self, origin, caller=None): 
		if type(origin) is Genome:
			self.subs = []
			self.genome = origin
			self.scored = False
			self.scores = {}
		elif type(origin) is Tree:

			self.genome = Genome(origin.genome)

			if caller is not None:
				self.subs = [Tree(sub,(origin,self) ) for sub in origin if sub is not caller[0]]
				self.subs.append(caller[1])

			else:
				self.subs = [Tree(sub, (origin,self) ) for sub in origin]

		self.scored = False
		self.scores = {}

	def __iter__( self ):
		return iter( self.subs )

	def __getitem__( self, key):
		return self.subs[key]

	def setGenome(self, g):
		self.scored = False
		self.scores = {} 
		self.genome = g

	def isBinary( self, caller=None):
		return True

	def allNodes( self, caller=None):
		s = self.genome.getName()
		s += " | "
		for sub in self: 
			s += sub.genome.getName()
			s += ", " 
		s += "\n"
		for sub in self:
			if sub is not caller:
				s += sub.allNodes(self)
		return s

	def isLeaf(self):
		return len(self.subs) in (0,1)

	def addConnection(self, other, caller=None ):
		self.scored = False
		self.scores = {}

		if type(other) is Tree:
			self.subs.append( other )
			if other is not caller:
				other.addConnection( self, self)
		elif type(other) is Genome:
			t = Tree( other )
			self.addConnection( t )
		else:
			raise Exception("Tried to add an invalid connection to a tree.")

	def breakConnection(self, other, caller=None):
		self.scored = False
		self.scores = {}

		self.subs.remove( other )
		if other is not caller:
			other.breakConnection( self, self )


	def getScore( self, caller=None):
		if self.scored and caller in self.scores:
			return self.scores[caller]

		else:
			if self.isLeaf() and caller is not None:
				return 0

			elif self.isLeaf() and caller is None:
				return self.subs[0].getScore()

			else:
				grimm = Grimm()
				s = 0
				for sub in self:
					if sub is not caller:
						s += sub.getScore( self )
						s += grimm.getDistance( self.genome, sub.genome)
				self.scores[caller] = s
				self.scored = True
				return s


	def getTips(self):
		tips = []

		def rTipFinder( t, tips, caller=None ):
			if t.isLeaf() and caller is not None:
				tips.append( t )

			elif t.isLeaf() and caller is None:
				tips.append(t)
				if not len(t.subs) == 0:
					rTipFinder( t.subs[0],tips, t)

			else:
				for sub in t:
					if sub is not caller:
						rTipFinder( sub , tips, t)

		rTipFinder(self , tips)
		return tips

	def __len__( self ):
		size = [0,]
		def rSizeFinder( t, size, caller=None ):
			size[0] += 1
			for sub in t:
				if sub is not caller:
					rSizeFinder( sub, size,  t)
		rSizeFinder(self ,size)
		return size[0]


	def toTuple( self, caller=None):
		if self.isLeaf() and caller is not None:
			return self

		elif self.isLeaf() and caller is None:
			return self.subs[0].toTuple()

		elif caller is None:
			return ( self.subs[0].toTuple(self), self.toTuple( self.subs[0] ))

		else:
			return tuple([sub.toTuple(self) for sub in self if sub is not caller])


	def __str__( self ):

		def rStringFinder( t, caller=None):
			if t.isLeaf() and caller is not None:
				return t.genome.getName()

			elif t.isLeaf() and caller is None:
				return rStringFinder( t.subs[0])

			elif caller is None:
				return "(" + rStringFinder(self.subs[0], self) + ", " + rStringFinder(self, self.subs[0]) + ")"

			else:

				s = "("
				for sub in t:
					if sub is not caller:
					 	s += rStringFinder( sub, t )
					 	s += ", "
				s = s[:-2]

				s += ")"
				return s

	
		return "Tree: " + rStringFinder(self )

	def genomeHash(self):
		return hash( self.genome )

	def getName(self):
		return self.genome.getName()



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
	aT.addConnection( bT)
	aT.addConnection( cT)
	print(aT)
	tips = aT.getTips()
	for tip in tips:
		print( tip )
	print( tips )
	print(tips[0].isLeaf())
	tips[0].addConnection(d)
	tips[0].addConnection(f)
	print(tips[0].isLeaf())
	print(str(tips[0]))
	print(aT)
	aT.addConnection( e)
	print(aT)
	print(bT)
	print(aT.toTuple())

if __name__ == "__main__":
	test()

	
