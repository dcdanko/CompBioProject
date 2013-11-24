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

	def isLeaf(self):
		return len(self.subs) in (0,1)

	def addConnection(self, other ):
		self.scored = False
		if type(other) is Tree:
			self.subs.append( other )
			other.addConnection( self)
		elif type(other) is Genome:
			t = Tree( other )
			self.addConnection( t )
		else:
			raise Exception("Tried to add an invalid connection to a tree.")

	def breakConnection(self, other):
		self.scored = False
		self.subs.remove( other )
		other.breakConnection( self )

	def getScore(self, caller=None):
		if self.scored:
			return self.score
		else:
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
			if t.isLeaf():
				tips.append( t )
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
			if t.isLeaf():
				return t
			else:
				l = []
				for sub in t:
					if sub is not caller:
						l.append( rTupFinder(sub,t))
				return tuple(l)

		return rTupFinder( self )

	def __str__( self ):

		def rStringFinder( t, caller=None):
			if t.isLeaf():
				return t.genome.getName() 
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

	
