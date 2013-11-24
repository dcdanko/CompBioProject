from Tree import Tree

def doNearestNeighbourInterchange( target, caller=None ):

	if caller is not None and not caller.isLeaf() and not target.isLeaf():

		scores = [target.getScore(),]

		if caller[0] is target:
			cSub = caller[1]
		else:
			cSub = caller[0]

		caller.breakConnection(cSub)
		target.addConnection(cSub)

		for tSub in target:
			if tSub is not caller and tSub is not cSub:
				target.breakConnection(tSub)
				caller.addConnection(tSub)
				scores.append( target.getScore() )

		assert len(scores) == 3

		if min(scores) == scores[2]:
			pass
		elif min(scores) == scores[1]:
			caller.addConnection( target[-1])
			target.addConnection( caller[-1])
			caller.breakConnection( caller[-1])
			target.breakConnection( target[-1])
		else:
			caller.addConnection( cSub )
			target.breakConnection( cSub )
			target.addConnection( caller[-1] )
			caller.breakConnection(caller[-1]) 

		assert target.getScore() == min(scores)

	for sub in target:
		doNearestNeighbourInterchange(sub, target)



