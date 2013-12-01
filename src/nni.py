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

	def calculate( self, timeout=300 ):
		self.timeout = timeout
		self.startTime = time()
		self.hits = {}
		self.doNNI( self.tree)



	def doNNI(self, target, caller=None, depth=0 ):
		# if caller is None:
		# 	print("Starting")

		# print( "Calling self.doNNI")

		if caller is None and target.isLeaf():
			# print("Started on leaf. Restarting.")
			self.doNNI(target.subs[0])

		elif caller is None and not target.isLeaf():
			# print("Started on internal node {}".format(target.genome.getName()))
			assert target.isBinary()
			self.doNNI(target, caller=target.subs[0], depth=depth+1)
			self.doNNI(target.subs[0], caller=target, depth=depth+1)

		elif caller is not None and target.isLeaf():
			# print("Hit leaf {} from {}".format(target.genome.getName(), caller.genome.getName()))
			pass

		elif caller is not None and not caller.isLeaf() and not target.isLeaf():
			if target in self.hits:
				return
			else:
				self.hits[target] = True
				
			# print("Hit internal node {} from {}".format(target.genome.getName(), caller.genome.getName()))
			# print("{} has connections to {}".format(target.genome.getName(), [s.genome.getName() for s in target]))
			grimm = Grimm()

			if len( caller.subs ) != 3:
				print caller.subs
				raise Exception("Caller has wrong number of connections")
			if len( target.subs ) != 3:
				print target.subs
				raise Exception("Target has wrong number of connections")

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
			
			# if A in self.hits or B in self.hits or C in self.hits or D in self.hits:
			# 	return
			# else:
			# 	self.hits[A] = True
			# 	self.hits[B] = True
			# 	self.hits[C] = True
			# 	self.hits[D] = True
			
			gAB = grimm.midGenome(A.genome, B.genome)
			gAC = grimm.midGenome(A.genome, C.genome)
			gAD = grimm.midGenome(A.genome, D.genome)
			gBC = grimm.midGenome(B.genome, C.genome)
			gBD = grimm.midGenome(B.genome, D.genome)
			gCD = grimm.midGenome(C.genome, D.genome)

			scores = [ 	
						grimm.getDistance(A.genome, B.genome) + grimm.getDistance(C.genome, D.genome) + grimm.getDistance(gAB, gCD),
						grimm.getDistance(A.genome, C.genome) + grimm.getDistance(B.genome, D.genome) + grimm.getDistance(gAC, gBD),
						grimm.getDistance(A.genome, D.genome) + grimm.getDistance(B.genome, C.genome) + grimm.getDistance(gAD, gBC),
					]

			if min(scores) == scores[0]:
				caller.setGenome( gAB )
				target.setGenome( gCD )

			elif min(scores) == scores[1]:
					caller.breakConnection(A)
					caller.breakConnection(B)
					target.breakConnection(C)
					target.breakConnection(D)

					caller.addConnection(A)
					caller.addConnection(C)
					target.addConnection(B)
					target.addConnection(D)

					caller.setGenome( gAC )
					target.setGenome( gBD )

			elif min(scores) == scores[2]:
					caller.breakConnection(A)
					caller.breakConnection(B)
					target.breakConnection(C)
					target.breakConnection(D)

					caller.addConnection(A)
					caller.addConnection(D)
					target.addConnection(B)
					target.addConnection(C)

					caller.setGenome( gAD )
					target.setGenome( gBC )

			else:
				raise Exception		

			assert caller.isBinary()
			assert target.isBinary()

			if time() - self.startTime < self.timeout and depth + 25 < getrecursionlimit():
				# for sub in target:
				# 	if sub is not caller:
				# 		for supersub in sub:
				# 			# print("Going to {} from {}".format(supersub.genome.getName(), sub.genome.getName()))
				# 			if supersub is not target:
				# 				self.doNNI(supersub,sub, depth + 1)
				# 			
				for sub in target:
					if sub is not caller:
						self.doNNI(sub, caller=target, depth=depth+1)
			elif depth < 5:
				print( "Timed Out, depth: {}".format(depth))

