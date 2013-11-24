from ArtificialDataGenerator import ArtificialPhylogeny
from PyGrimmInterface import GrimmInterface
from upgma_tree import UPGMA
from genome import Genome
from Tree import Tree
import random as rn

def fastRobinsonFouldsDistance(a,b):

	# Trees are represented as tuples (0, (1, (2, (3,4))))

	labels = {}

	def recursive_labeling(val, parts):
		if(type(val) is Tree):
			if(val in labels):
				return labels[val]
			else:
				labels[val] = rn.randint(0,2**64)
				return recursive_labeling(val,parts)
		else:
			assert len(val) == 2
			newPartition = recursive_labeling(val[0], parts) ^ recursive_labeling(val[1], parts)
			if(type(parts)  == dict):
				parts[ newPartition ] = True
			else:
				parts.append(newPartition)
			return newPartition

	aParts = {}
	recursive_labeling(a, aParts)
	bParts = {}
	recursive_labeling(b, bParts)
	distance = 0
	for val in aParts:
		if val not in bParts:
			distance += 1
	
	return distance



def testOne():
	a = ArtificialPhylogeny(size=100,numChromosomes=10)
	for arb in range(5):
		a.evolve()

	u = UPGMA( [t.genome for t in a.tree.getTips()])
	u.calculate()

	rf = fastRobinsonFouldsDistance(a.tree.toTuple(), u.tree.toTuple())
	return (rf, len( u.tree ) - 3)

def testTwo():
	a = ArtificialPhylogeny(size=1000,numChromosomes=10)
	for arb in range(5):
		a.evolve()

	u = UPGMA( [t.genome for t in a.tree.getTips()])
	u.calculate()

	rf = fastRobinsonFouldsDistance(a.tree.toTuple(), u.tree.toTuple())
	return (rf, len( u.tree ) - 3)

def testThree():
	a = ArtificialPhylogeny(size=100,numChromosomes=10)
	for arb in range(10):
		a.evolve()

	u = UPGMA( [t.genome for t in a.tree.getTips()])
	u.calculate()

	rf = fastRobinsonFouldsDistance(a.tree.toTuple(), u.tree.toTuple())
	return (rf, len( u.tree ) - 3)

def testFour():
	a = ArtificialPhylogeny(size=1000,numChromosomes=10)
	for arb in range(10):
		a.evolve()

	u = UPGMA( [t.genome for t in a.tree.getTips()])
	u.calculate()

	rf = fastRobinsonFouldsDistance(a.tree.toTuple(), u.tree.toTuple())
	return (rf, len( u.tree ) - 3)
def grimmTest():
	a = ArtificialPhylogeny(size=2*1000,numChromosomes=10)
	genomes = []
	while(len(a.tree.getTips()) < 25):
		a.evolve()	
	for tip in  a.tree.getTips():
		genomes.append(tip.genome)	

	grimm = GrimmInterface()
	estimatedroot = grimm.findRootViaUPGMA(genomes)
	original = a.original

	transformations = grimm.getTransformations(estimatedroot, original)
	distance = len(transformations)-1
	# print "estimate: "+str(estimatedroot)
	print "GRIMM Distance: {}".format(distance)

# grimmTest()
if __name__ == "__main__":
	val = 0.0
	maxSize = 0.0
	k = 20
	for arb in range(k):
		try:
			(a,b) = testOne()
			val += a
			maxSize += b
		except: 
			pass
	print ( val/k, maxSize/k)
	val = 0.0
	maxSize = 0.0
	k = 20
	for arb in range(k):
		try:
			(a,b) = testTwo()
			val += a
			maxSize += b
		except:
			pass
	print ( val/k, maxSize/k)
	val = 0.0
	maxSize = 0.0
	k = 20
	for arb in range(k):
		try:
			(a,b) = testThree()
			val += a
			maxSize += b
		except:
			pass
	print ( val/k, maxSize/k)
	val = 0.0
	maxSize = 0.0
	k = 20
	for arb in range(k):
		try:
			(a,b) = testFour()
			val += a
			maxSize += b
		except:
			pass
	print ( val/k, maxSize/k)

