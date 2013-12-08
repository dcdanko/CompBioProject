from Tree import Tree
from PyGrimmInterface import GrimmInterface as Grimm
from time import time
from sys import getrecursionlimit


class NNI( object ):

	def __init__(self, initialTree):
		self.tree = initialTree
		self.score = initialTree.getScore()
		self.grimm = Grimm()
		self.trees = [self.tree,]
		self.splitThreshold = 3

	def calculate( self, timeout=300 ,deepScoring=True):
		self.deepScoring = deepScoring
		self.timeout = timeout * len(self.trees)
		self.startTime = time()
		self.hits = {}
		for t in self.trees:
			self.doNNI( t)


	def doNNI(self, target, caller=None, depth=0, blockSplits=False):

		newGenomeScoring = False

		timedOut = time() - self.startTime > self.timeout
		tooDeep = depth + 50 > getrecursionlimit()

		if caller is None and target.isLeaf():
			self.doNNI(target.subs[0])

		elif caller is None and not target.isLeaf():
			self.doNNI(target, caller=target[0],depth=1)
			self.doNNI(target[0], caller=target,depth=1)

		elif caller is not None and target.isLeaf():
			return 

		elif caller is not None and not caller.isLeaf() and not target.isLeaf():
			
			if target in self.hits:
				self.hits[target] += 1
			else:
				self.hits[target] = 1

			A, B, C, D = self.getSubtrees(target, caller)
			
			if newGenomeScoring:
				gAB, gAC, gAD, gBC, gBD, gCD = self.getNewGenomes(A,B,C,D)

			if newGenomeScoring:

				scores = [ 	
							self.grimm.getDistance(A.genome, B.genome) + self.grimm.getDistance(C.genome, D.genome) + self.grimm.getDistance(gAB, gCD),
							self.grimm.getDistance(A.genome, C.genome) + self.grimm.getDistance(B.genome, D.genome) + self.grimm.getDistance(gAC, gBD),
							self.grimm.getDistance(A.genome, D.genome) + self.grimm.getDistance(B.genome, C.genome) + self.grimm.getDistance(gAD, gBC),
						]

			elif self.deepScoring:

				scores = []

				self.switchToConformer(target,caller,0,A,B,C,D)
				scores.append(target.getScore())

				self.switchToConformer(target,caller,1,A,B,C,D)
				scores.append(target.getScore())

				self.switchToConformer(target,caller,2,A,B,C,D)
				scores.append(target.getScore())


			else:

				scores = [ 	
							self.grimm.getDistance(A.genome, B.genome) + self.grimm.getDistance(C.genome, D.genome), 
							self.grimm.getDistance(A.genome, C.genome) + self.grimm.getDistance(B.genome, D.genome),
							self.grimm.getDistance(A.genome, D.genome) + self.grimm.getDistance(B.genome, C.genome),
						]

			if min(scores) == scores[0]:

				self.switchToConformer(target,caller,0,A,B,C,D)

				if not blockSplits and min(scores) in scores[1:] and len(self.trees) < self.splitThreshold:
					# print("NNI: splitting from 0 at depth {}. Scores: {}".format(depth, scores))
					# print("There are {} trees".format(len(self.trees)))
					splitTree = Tree(target)
					self.trees.append( splitTree)
					#wont work with genome update
					if not timedOut and not tooDeep:
						for sub in splitTree:
							assert splitTree in sub.subs
							assert sub in splitTree.subs
							if sub.genome.getName() != caller.genome.getName() and sub not in self.hits:
								self.doNNI(sub, caller=splitTree, depth=depth+1, blockSplits=True)


			if min(scores) == scores[1]:

					self.switchToConformer(target,caller,1,A,B,C,D)

					if not blockSplits and min(scores) == scores[2] and len(self.trees) < self.splitThreshold:
						# print("NNI: splitting from 1 at depth {}. Scores: {}".format(depth, scores))
						# print("There are {} trees".format(len(self.trees)))

						splitTree = Tree(target)
										
						self.trees.append( splitTree)
						#wont work with genome update
						if not timedOut and not tooDeep:
							for sub in splitTree:
								assert splitTree in sub.subs
								assert sub in splitTree.subs
								if sub.genome.getName() != caller.genome.getName() and sub not in self.hits:
									self.doNNI(sub, caller=splitTree, depth=depth+1, blockSplits=True)

			if min(scores) == scores[2]:
					
					self.switchToConformer(target,caller,2,A,B,C,D)

			if not timedOut and not tooDeep:
				for sub in target:
					if sub is not caller and sub not in self.hits:
						self.doNNI(sub, caller=target, depth=depth+1)


	def switchToConformer(self, target, caller, conformer, A,B,C,D):
		if conformer == 0:
			if A not in caller.subs:
				caller.addConnection(A)
			if B not in caller.subs:
				caller.addConnection(B)
			if C in caller.subs:
				caller.breakConnection(C)
			if D in caller.subs:
				caller.breakConnection(D)

			if C not in target.subs:
				target.addConnection(C)
			if D not in target.subs:
				target.addConnection(D)
			if A in target.subs:
				target.breakConnection(A)
			if B in target.subs:
				target.breakConnection(B)

		elif conformer == 1:
			if A not in caller.subs:
				caller.addConnection(A)
			if C not in caller.subs:
				caller.addConnection(C)
			if B in caller.subs:
				caller.breakConnection(B)
			if D in caller.subs:
				caller.breakConnection(D)

			if B not in target.subs:
				target.addConnection(B)
			if D not in target.subs:
				target.addConnection(D)
			if A in target.subs:
				target.breakConnection(A)
			if C in target.subs:
				target.breakConnection(C)

		if conformer == 2:
			if A not in caller.subs:
				caller.addConnection(A)
			if D not in caller.subs:
				caller.addConnection(D)
			if C in caller.subs:
				caller.breakConnection(C)
			if B in caller.subs:
				caller.breakConnection(B)

			if C not in target.subs:
				target.addConnection(C)
			if B not in target.subs:
				target.addConnection(B)
			if A in target.subs:
				target.breakConnection(A)
			if D in target.subs:
				target.breakConnection(D)


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
			raise Exception("Caller and target are not connected")

		if target[0] is caller:
			C,D = target[1], target[2]
		elif target[1] is caller:
			C,D = target[0], target[2]
		elif target[2] is caller:
			C,D = target[0], target[1]
		else:
			raise Exception("Target and caller are not connected")

		return (A,B,C,D)







