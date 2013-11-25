from Tree import Tree
from PyGrimmInterface import GrimmInterface as Grimm

def doNNI( target, caller=None ):

	if caller is not None and not caller.isLeaf() and not target.isLeaf():

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

		caller.breakConnection(A)
		caller.breakConnection(B)
		target.breakConnection(C)
		target.breakConnection(D)

		caller.addConnection(A)
		caller.addConnection(B)
		target.addConnection(C)
		target.addConnection(D)

		caller.setGenome( grimm.midGenome(A.genome,B.genome) )
		target.setGenome( grimm.midGenome(C.genome,D.genome) )

		# for sub in target:
		# 	if sub is not caller:
		# 		doNNI(sub, target)

		scores = [ caller.getScore(), ]

		caller.breakConnection(A)
		caller.breakConnection(B)
		target.breakConnection(C)
		target.breakConnection(D)

		caller.addConnection(A)
		caller.addConnection(C)
		target.addConnection(B)
		target.addConnection(D)

		caller.setGenome( grimm.midGenome(A.genome,C.genome) )
		target.setGenome( grimm.midGenome(B.genome,D.genome) )
		# for sub in target:
		# 	if sub is not caller:
		# 		doNNI(sub, target)

		scores.append( caller.getScore() )

		caller.breakConnection(A)
		caller.breakConnection(C)
		target.breakConnection(B)
		target.breakConnection(D)

		caller.addConnection(A)
		caller.addConnection(D)
		target.addConnection(B)
		target.addConnection(C)

		caller.setGenome( grimm.midGenome(A.genome,D.genome) )
		target.setGenome( grimm.midGenome(C.genome,B.genome) )

		# for sub in target:
		# 	if sub is not caller:
		# 		doNNI(sub, target)

		scores.append( caller.getScore() )

		caller.breakConnection(A)
		caller.breakConnection(D)
		target.breakConnection(B)
		target.breakConnection(C)



		if min(scores) == scores[0]:
			caller.addConnection(A)
			caller.addConnection(B)
			target.addConnection(C)
			target.addConnection(D)

			caller.setGenome( grimm.midGenome(A.genome,B.genome) )
			target.setGenome( grimm.midGenome(C.genome,D.genome) )

			trace = "zero"

		elif min(scores) == scores[1]:
			caller.addConnection(A)
			caller.addConnection(C)
			target.addConnection(B)
			target.addConnection(D)

			caller.setGenome( grimm.midGenome(A.genome,C.genome) )
			target.setGenome( grimm.midGenome(B.genome,D.genome) )

			trace = "one"

		else:
			caller.addConnection(A)
			caller.addConnection(D)
			target.addConnection(B)
			target.addConnection(C)

			caller.setGenome( grimm.midGenome(A.genome,D.genome) )
			target.setGenome( grimm.midGenome(C.genome,B.genome) )

			trace = "two"

		if target.getScore() - min(scores) > 1:
			print scores
			print( target.getScore() )
			print caller.getScore()
			print trace
			print target 
			# raise Exception("Tree is not minimum cost.")
			print "Tree is not minimum cost"

	for sub in target:
		if sub is not caller:
			doNNI(sub, target)



