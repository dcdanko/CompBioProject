from ArtificialDataGenerator import ArtificialPhylogeny
from PyGrimmInterface import GrimmInterface
from upgma_tree import UPGMA
from genome import Genome
from Tree import Tree
import random as rn
from nni import doNNI
import matplotlib.pyplot as plt
from pylab import savefig


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
			if len(val) != 2:
				print( val)
				raise Exception("Val is wrong length")
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


def testTrees():
	a = ArtificialPhylogeny(size=20,numChromosomes=5)
	while len(a.tree.getTips()) < 6:
		a.evolve()
	tipScores = [tip.getScore() for tip in a.tree.getTips()]
	s = a.tree.getScore()
	tipScores = [score -s for score in tipScores]
	for score in tipScores:
		assert score == 0

	sub = a.tree.subs[0]
	a.tree.breakConnection( sub )
	a.tree.addConnection( sub)

	tipScores = [tip.getScore() for tip in a.tree.getTips()]
	s = a.tree.getScore()
	tipScores = [score -s for score in tipScores]
	for score in tipScores:
		assert score == 0

	aTips = a.tree.getTips()
	subTips = a.tree.subs[0].getTips()
	for tip in aTips:
		assert tip in subTips

	print("All tree tests passed.")




def upgmaHarness(cSize,depth):
	a = ArtificialPhylogeny(size=cSize,numChromosomes=10)
	while len(a.tree.getTips()) < depth:
		a.evolve()

	u = UPGMA( [t.genome for t in a.tree.getTips()])
	u.calculate()

	rf = fastRobinsonFouldsDistance(a.tree.toTuple(), u.tree.toTuple())
	return (rf, len( u.tree ) - 3)

def testUPGMA():
	print( "Testing UPGMA trees")
	rf, maxRF= 0,0
	rfs, maxRFs= [], []
	k = 2
	for depth in range(5,21,5):
		for arb in range(k):
			(a,b) = upgmaHarness(100,depth)
			rf += a
			maxRF += b
		rfs.append( rf/k)
		maxRFs.append(maxRF/k)

	print("R.F. Distance:     {}".format(rfs))
	print("Max R.F. Distance: {}".format(maxRFs))

def graphUPGMA():
	rf, maxRF = 0,0
	rfs, maxRFs = [], []
	k = 25
	for depth in range(5,51,5):
		for arb in range(k):
			(a,b) = upgmaHarness(100,depth)
			rf += a
			maxRF += b
		rfs.append( rf/k)
		maxRFs.append(maxRF/k)

	plt.figure("Robinson Foulds Scores of UPGMA trees as a function of the number of tips")
	plt.plot(range(5,51,5),rfs)
	plt.plot(range(5,51,5),maxRFs)
	savefig("RF_Artificial_UOGMA.png")


def nniHarness(cSize,depth):
	a = ArtificialPhylogeny(size=cSize,numChromosomes=10)
	while len( a.tree.getTips() ) < depth:
		a.evolve()

	if not a.tree.isBinary():
		print len(a.tree)
		print [ t.genome.getName() for t in a.tree.getTips()]
		print a.tree.allNodes()
		print a.tree
		raise Exception("Artificial Phylogeny is not binary")


	u = UPGMA( [t.genome for t in a.tree.getTips()])
	u.calculate()

	tree = u.tree 
	assert tree.isBinary()

	uRF = fastRobinsonFouldsDistance(a.tree.toTuple(), tree.toTuple())
	uScore = tree.getScore()
	doNNI( tree )
	nScore = tree.getScore()
	nRF = fastRobinsonFouldsDistance(a.tree.toTuple(), tree.toTuple())

	return (nRF, uRF, len(tree) - 3, uScore, nScore, a.tree.getScore())

def testNNI():
	print("Testing NNI trees.")
	nrf, urf, maxRF, uScore, nScore, aScore = 0,0,0,0,0,0
	nrfs, urfs, maxRFs, uScores, nScores, aScores = [], [], [], [], [], []
	k = 1
	for depth in range(4,10,2):
		for arb in range(k):
			(a,b,c,d,e,f) = nniHarness(100,depth)
			nrf += a
			urf += b
			maxRF += c
			uScore += d
			nScore += e
			aScore += f
			print( "Just finished a tree with {} tips".format(depth) )

		nrfs.append( nrf/k)
		urfs.append( urf/k)
		maxRFs.append(maxRF/k)
		uScores.append(uScore/k)
		nScores.append(nScore/k)
		aScores.append(aScore/k)

		print("R.F. Distance with NNI:   {}".format(nrfs))
		print("R.F. Distance with UPGMA: {}".format(urfs))
		print("Max R.F. Distance:        {}".format(maxRFs))
		print("Tree scores with NNI:   {}".format(nScores))
		print("Tree scores with UPGMA: {}".format(uScores))
		print("Actual Tree scores:     {}".format(aScores))




if __name__ == "__main__":
	testTrees()

	testUPGMA()

	testNNI()


