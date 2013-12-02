from Tree import Tree
from PyGrimmInterface import GrimmInterface as Grimm
from time import time
from copy import deepcopy
from sys import getrecursionlimit

class NNI( object ):

	def __init__(self, initialTree):
		self.tree = initialTree
		self.score = initialTree.getScore()
		self.grimm = Grimm()
		self.trees = [self.tree,]

	def calculate( self, timeout=300 ):
		self.timeout = timeout
		self.startTime = time()
		self.hits = {}
		self.doNNI( self.tree)


	def doNNI(self, target, caller=None, depth=0):

		genomeUpdate = False
		newGenomeScoring = False
		timedOut = time() - self.startTime > self.timeout
		tooDeep = depth + 50 > getrecursionlimit()

		if caller is None and target.isLeaf():
			self.doNNI(target.subs[0])

		elif caller is None and not target.isLeaf():
			self.doNNI(target, caller=target.subs[0],depth=1)
			self.doNNI(target.subs[0], caller=target,depth=1)

		elif caller is not None and target.isLeaf():
			return 

		elif caller is not None and not caller.isLeaf() and not target.isLeaf():
			
			if target in self.hits:
				self.hits[target]

			A, B, C, D = self.getSubtrees(target, caller)
			
			if genomeUpdate or newGenomeScoring:
				gAB, gAC, gAD, gBC, gBD, gCD = self.getNewGenomes(A,B,C,D)

			if newGenomeScoring:

				scores = [ 	
							self.grimm.getDistance(A.genome, B.genome) + self.grimm.getDistance(C.genome, D.genome) + self.grimm.getDistance(gAB, gCD),
							self.grimm.getDistance(A.genome, C.genome) + self.grimm.getDistance(B.genome, D.genome) + self.grimm.getDistance(gAC, gBD),
							self.grimm.getDistance(A.genome, D.genome) + self.grimm.getDistance(B.genome, C.genome) + self.grimm.getDistance(gAD, gBC),
						]

			else:

				scores = [ 	
							self.grimm.getDistance(A.genome, B.genome) + self.grimm.getDistance(C.genome, D.genome), 
							self.grimm.getDistance(A.genome, C.genome) + self.grimm.getDistance(B.genome, D.genome),
							self.grimm.getDistance(A.genome, D.genome) + self.grimm.getDistance(B.genome, C.genome),
						]

			if min(scores) == scores[0]:

				if genomeUpdate:
					caller.setGenome( gAB )
					target.setGenome( gCD )
				else:
					pass

				if min(scores) in scores[1:]:
					self.trees.append( deepcopy(target))
					#wont work with genome update
					if not timedOut and not tooDeep:
						for sub in self.trees[-1]:
							if sub.genome.getName() != caller.genome.getName and sub not in self.hits:
								self.doNNI(sub, caller=self.trees[-1], depth=depth+1)


			if min(scores) == scores[1]:
					caller.breakConnection(A)
					caller.breakConnection(B)
					target.breakConnection(C)
					target.breakConnection(D)

					caller.addConnection(A)
					caller.addConnection(C)
					target.addConnection(B)
					target.addConnection(D)

					if genomeUpdate:
						caller.setGenome( gAC )
						target.setGenome( gBD )

					if min(scores) == scores[2]:
						self.trees.append( deepcopy(target))

						caller.breakConnection(A)
						caller.breakConnection(C)
						target.breakConnection(B)
						target.breakConnection(D)

						caller.addConnection(A)
						caller.addConnection(B)
						target.addConnection(C)
						target.addConnection(D)
						if not timedOut and not tooDeep:
							for sub in self.trees[-1]:
								if sub.genome.getName() != caller.genome.getName and sub not in self.hits:
									self.doNNI(sub, caller=self.trees[-1], depth=depth+1)

			if min(scores) == scores[2]:
					caller.breakConnection(A)
					caller.breakConnection(B)
					target.breakConnection(C)
					target.breakConnection(D)

					caller.addConnection(A)
					caller.addConnection(D)
					target.addConnection(B)
					target.addConnection(C)

					if genomeUpdate:
						caller.setGenome( gAD )
						target.setGenome( gBC )

			if not timedOut and not tooDeep:
				for sub in target:
					if sub is not caller and sub not in self.hits:
						self.doNNI(sub, caller=target, depth=depth+1)



	def getNewGenomes(self, A,B,C,D ):
		gAB = self.grimm.midGenome(A.genome, B.genome)
		gAC = self.grimm.midGenome(A.genome, C.genome)
		gAD = self.grimm.midGenome(A.genome, D.genome)
		gBC = self.grimm.midGenome(B.genome, C.genome)
		gBD = self.grimm.midGenome(B.genome, D.genome)
		gCD = self.grimm.midGenome(C.genome, D.genome)

		return (gAB, gAC, gAD, gBC, gBD, gCD)

	def getSubtrees(self, target, caller):
		if caller[0] is target:
			A,B = caller[1], caller[2]
		elif caller[1] is target:
			A,B = caller[0], caller[2]
		elif caller[2] is target:
			A,B = caller[0], caller[1]
		else:
			raise Exception("Caller and target not connected")

		if target[0] is caller:
			C,D = target[1], target[2]
		elif target[1] is caller:
			C,D = target[0], target[2]
		elif target[2] is caller:
			C,D = target[0], target[1]
		else:
			raise Exception("Caller and target not connected")

		return (A,B,C,D)

	def cull(self):
		bestScore = 1000*1000
		bestTrees = []
		for tree in self.trees:
			if tree.getScore() < bestScore:
				bestScore = tree.getScore()
				bestTrees = [tree, ]
			elif tree.getScore() == bestScore:
				bestTrees.append(tree)
		self.trees = bestTrees

	def buildConsensusTree(self):
		consensusThreshold = .51

		self.cull()
		partitionsToSubs = {}
		tipsToLabels = {}
		parts = {}
		numTrees = 1.0*len(self.trees)

		for tip in self.trees[0]:
			tipsToLabels[tip] = rn.randint(0,2**64)

		def rParter( tree, caller=None):
			if tree.isLeaf() and caller is None:
				rParter(tree[0])

			elif tree.isLeaf():
				partitionsToSubs[tipsToLabels[tree]] = 
				return tipsToLabels[tree]

			elif caller is None:
				parts[tree] = [rParter(target,target[0]),rParter(target[0],target)]

			else:
				out = 0
				for sub in tree:
					if sub is not caller:
						out = out ^ rParter( sub, tree)
				parts[tree] = out
				return out


		for tree in self.trees:
			rParter( tree)

		countParts = {}
		for tree in self.trees:
			for part in parts[tree]:
				if part in countParts:
					countParts[part] += 1
				else:
					countParts[part] = 1

		partsToKeep = []

		for part, count in countParts.items():
			if count/numTrees > consensusThreshold:
				partsToKeep.append(part)


