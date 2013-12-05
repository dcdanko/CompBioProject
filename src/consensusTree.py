from random import randint
from Tree import Tree
from genome import Genome
from PyGrimmInterface import GrimmInterface as Grimm

def getMatrixMin(matrix):
	(width, height) = matrix.shape
	minimum, x, y = -1,0,0
	for i in range(width):
		for j in range(i+1, height):
			if minimum == -1 or matrix[i,j] < minimum:
				minimum = matrix[i,j]
				x, y= i, j
	assert x != y
	return (x,y)



class ConsensusTree( object ):

	def __init__(self, trees):
		self.trees = trees
		self.grimm = Grimm()

	def cull(self):
		bestScore = 1000*1000*1000
		bestTrees = []
		for tree in self.trees:

			if tree.getScore() < bestScore:
				bestScore = tree.getScore()
				bestTrees = [tree, ]
			elif tree.getScore() == bestScore:
				bestTrees.append(tree)
		self.trees = bestTrees
		

	def calculate(self):
		consensusThreshold = .51

		self.cull()
		if len(self.trees) == 1:
			self.conTree = self.trees[0]
			return 

		partsToSubs = {}
		tipGenomesToLabels = {}
		labelsToTips = {}
		parts = {}
		numTrees = 1.0*len(self.trees)
		topLabel = 0

		for tip in self.trees[0].getTips():
			newLabel = randint(0,2**64)
			h = str( hash(tip.genome)) + tip.genome.getName()
			tipGenomesToLabels[h] = newLabel
			labelsToTips[newLabel] = Tree(tip.genome)




		for tree in self.trees[:]:
			topLabel = self.rParter( tree, partsToSubs, parts, tipGenomesToLabels)
			
	

		countParts = {}
		for tree in self.trees:
			for part in parts[tree]:
				if part in countParts:
					countParts[part] += 1
				else:
					countParts[part] = 1

		partsToKeep = []

		partsToKeep.append(topLabel)

		for part, count in countParts.items():
			if count/numTrees > consensusThreshold:
				partsToKeep.append(part)


		self.conTree = self.rTreeBuilder(topLabel, partsToSubs, labelsToTips, partsToKeep)[0]

		self.genomeEstimator( self.conTree ) # Note: different consensus trees could develop from different starts
		


	def rTreeBuilder(self, keyLabel, partsToSubs, labelsToTips, partsToKeep):
		subLabels = partsToSubs[keyLabel]

		if subLabels == "TIP":
			return [ labelsToTips[keyLabel], ]

		elif keyLabel in partsToKeep:
			newTree = Tree( Genome(name='place holder'))
			
			for sLabel in subLabels:
				sTrees = self.rTreeBuilder(sLabel, partsToSubs, labelsToTips, partsToKeep)
				for t in sTrees:
					newTree.addConnection(t)
			return [newTree]
		
		else:
			out = []
			for sLabel in subLabels:
				out += self.rTreeBuilder(sLabel, partsToSubs, labelsToTips, partsToKeep)
			return out


		

	def rParter(self, tree, partsToSubs, parts, tipGenomesToLabels, caller=None, originalTree=None):

		if tree.isLeaf() and caller is None:

			self.trees.remove(tree)
			self.trees.append(tree[0])
			return self.rParter(tree[0], partsToSubs, parts, tipGenomesToLabels)

		elif tree.isLeaf():

			h = str( hash(tree.genome)) + tree.genome.getName()
			tipLabel = tipGenomesToLabels[h]
			partsToSubs[tipLabel] = "TIP"

			return tipLabel

		elif caller is None:

			parts[tree] = []
			l = self.rParter(tree, partsToSubs, parts, tipGenomesToLabels, caller=tree[0],originalTree=tree)
			r = self.rParter(tree[0], partsToSubs, parts, tipGenomesToLabels, caller=tree,originalTree=tree)
			parts[tree].append(l)
			parts[tree].append(r)

			keyLabel = l ^ r
			partsToSubs[keyLabel] = [l,r]
			return keyLabel

		else:

			out = 0
			subLabels = []
			for sub in tree:
				if sub is not caller:
					label = self.rParter( sub, partsToSubs, parts, tipGenomesToLabels, caller=tree,originalTree=originalTree)
					subLabels.append( label)
					out = out ^ label

			parts[originalTree].append(out)
			partsToSubs[out] = subLabels

			return out

	def genomeEstimator(self, tree, caller=None):
		
		if caller is None and tree.isLeaf():
			self.genomeEstimator(tree[0])

		elif tree.genome.name != "place holder":
			return

		elif caller is None:
			for subTree in tree:
				self.genomeEstimator(subTree, tree)

			if len(tree.subs) == 3:
				
				edgeMidA = self.grimm.midGenome(tree[1].genome, tree[2].genome)
				tSetA = self.grimm.getTransformations(tree.subs[0].genome, edgeMidA)
				tSetA = [tran[1] for tran in tSetA]
				
				edgeMidB = self.grimm.midGenome(tree[0].genome, tree[2].genome)
				tSetB = self.grimm.getTransformations(tree.subs[1].genome, edgeMidB)
				tSetB = [tran[1] for tran in tSetB]
				
				pairDists = [self.grimm.getDistance(tSetA[i], tSetB[i]) for i in range(min( len(tSetA), len(tSetB)))]
				mindex = pairDists.index( min(pairDists) )
				newGenome = self.grimm.midGenome( tSetA[mindex], tSetB[mindex] )
				
				tree.setGenome(newGenome)

			elif len(tree.subs) == 2:

				tree.setGenome(tree[1].genome)

				subs = [sub for sub in tree[1]]
				
				for sub in subs:
					if sub is not tree:
						tree.addConnection(sub)
						tree[1].breakConnection(sub)

				
				tree.breakConnection( tree[1])


				self.genomeEstimator(tree)


			else:

				m = self.grimm.getDistMatrix( [s.genome for s in tree])
				(minX, minY) = getMatrixMin(m)
				newSubTree = Tree( Genome( name="place holder"))
				a, b = tree[minX], tree[minY]
				newSubTree.addConnection(a)
				newSubTree.addConnection(b)
				tree.breakConnection(a)
				tree.breakConnection(b)
				tree.addConnection(newSubTree)

				self.genomeEstimator(tree)

		elif not tree.isLeaf():

			for subTree in tree:
				if subTree is not caller:
					self.genomeEstimator(subTree, tree)

			subTrees = [sub for sub in tree if sub is not caller]

			if len(subTrees) == 2:
				newGenome = self.grimm.midGenome( subTrees[0].genome, subTrees[1].genome )
				tree.setGenome(newGenome)

			else:

				m = self.grimm.getDistMatrix( [s.genome for s in subTrees])
				(minX, minY) = getMatrixMin(m)
				a, b = subTrees[minX], subTrees[minY]


				newSubTree = Tree( Genome( name="place holder"))

				a, b = subTrees[minX], subTrees[minY]
				newSubTree.addConnection(a)
				newSubTree.addConnection(b)


				tree.breakConnection(a)
				tree.breakConnection(b)

				tree.addConnection(newSubTree)

				self.genomeEstimator(tree, caller)


