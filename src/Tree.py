from genome import Genome
from PyGrimmInterface import GrimmInterface as Grimm


class Tree( object ):

	def __init__(self, genome): 
		if type(genome) is Genome:
			self.subs = []
			self.genome = genome
			self.scored = False

	def __iter__( self ):
		return iter( self.subs )

	def __getitem__( self, key):
		return self.subs[key]

	def setGenome(self, g):
		self.scored = False
		self.genome = g

	def isBinary( self, caller=None):
		if self.isLeaf() and caller is not None:
			return True

		elif self.isLeaf() and caller is None:
			b = True
			for sub in self:
				b *= sub.isBinary( self )
			return b

		elif len( self.subs) != 3:
			return False

		else:
			b = True
			for sub in self:
				if sub is not caller:
					b *= sub.isBinary( self )
			return b

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
		self.subs.remove( other )
		if other is not caller:
			other.breakConnection( self, self )

	def getScore(self, caller=None):
		if self.scored :
			return self.score
		else:
			
			if self.isLeaf() and caller is not None:
				return 0
			elif self.isLeaf() and caller is None:
				return self.subs[0].getScore()

			grimm = Grimm()
			score = 0
			for sub in self:
				if sub is not caller:
					score += sub.getScore( self )
					score += grimm.getDistance( self.genome, sub.genome) 
			self.score = score
			self.scored = True
			return score


	def getTips(self):
		tips = []

		def rTipFinder( t, tips, caller=None ):
			if t.isLeaf() and caller is not None:
				tips.append( t )
			elif t.isLeaf() and caller is None:
				tips.append( t )
				for sub in t:
					rTipFinder( sub, tips, t)
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

	def toTuple( self ):

		def rTupFinder( t, caller= None):
			if t.isLeaf() and caller is not None:
				return t
			elif t.isLeaf() and caller is None:
				l = [t,]
				for sub in t:
					if sub is not caller:
						l.append( rTupFinder(sub,t))
				return tuple(l)
			elif caller is None:
				return (rTupFinder(t.subs[0],t),(rTupFinder(t.subs[1],t),rTupFinder(t.subs[2],t) ) )
			else:
				l = []
				for sub in t:
					if sub is not caller:
						l.append( rTupFinder(sub,t))
				return tuple(l)

		return rTupFinder( self )

	def __str__( self ):

		def rStringFinder( t, caller=None):
			if t.isLeaf() and caller is not None:
				return t.genome.getName() 
			else:

				s = "("
				if t.isLeaf():
					s += t.genome.getName() +", "
				for sub in t:
					if sub is not caller:
					 	s += rStringFinder( sub, t )
					 	s += ", "
				s = s[:-2]

				s += ")"
				return s

	
		return "Tree: " + rStringFinder(self )





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

	
