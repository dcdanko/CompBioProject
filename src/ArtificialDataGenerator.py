import random as rn
from genome import Genome
from tree import Tree

class ArtificialPhylogeny( object ):


	def __init__( self, size=5, numChromosones=3):
		self.original = Genome()
		for c in range( numChromosones ):
			for pos in range(size):
				chromosone = ""
				for val in range( c*size, (c+1)*size ):
					chromosone += str(val)
					chromosone += " "
				self.original.addChromosone(chromosone)

		self.tree = Tree( self.original )


	def produceDescendant(self, ancestor ):
		mod = rn.choice(["DELETION", "DUPLICATION", "MOVEMENT","NONE"])
		descendant = [a for a in ancestor]

		if mod == "DELETION":
			descendant.pop( rn.randint(0,len(descendant)-1))

		elif mod == "DUPLICATION":
			dup = rn.choice( descendant )
			descendant.insert( rn.randint(0,len(descendant)-1), dup)

		elif mod == "MOVEMENT":
			dup = rn.choice( descendant )
			descendant.remove( dup )
			descendant.insert( rn.randint(0,len(descendant)-1), dup)

		elif mod == "NONE":
			pass

		return (mod, descendant)

	def mutate(self, ancestor):
		mod = rn.choice( ["REVERSAL", "TRANSLOCATION"] )
		if mod == "REVERSAL":
			chromosone = rn.choice(ancestor)
			start = rn.randrange(len(chromosone))
			end = rn.randrange( start, len(chromosone))
			tempChromosone = chromosone[:]

			for i, val in enumerate(tempChromosone):
				if i >= start and i <= end:
					chromosone[i] = tempChromosone[end - i + 1]

		elif mod == "TRANSLOCATION":
			(chrA, chrB) = rn.sample(anestor,2)
			stA,stB = rn.choice(len(chrA)) ,rn.choice(len(chrB))
			enA,enB = rn.choice(stA,len(chrA)) ,rn.choice(stB,len(chrB))

			transA= [a for i, a in enumerate(chrA) if i >= stA and i <=enA]
			if rn.random() < 0.5:
				transA = transA[::-1]

			transB= [b for i, b in enumerate(chrB) if i >= stB and i <=enB]
			if rn.random() < 0.5:
				transB = transB[::-1]

			frontA, backA, frontB, backB = chrA[:stA], chrA[enA+1:], chrB[:stB], chrB[enB+1:]
			tempA, tempB = frontA+transB+backA, frontB+transA+backB

			for i,val in enumerate(tempA):
				chrA[i] = val
			for i,val in enumerate(tempB):
				chrB[i] = val
					

		return ancestor

	def evolve(self, evolutionRate=0.5):
		tips = []
		self.tree.populateTips(tips)
		for (genome, leaf) in tips:
			if rn.random() < evolutionRate:
				newGenome = Genome( genome=genome )
				mutate( newGenome )

				if rn.random() < evolutionRate:
					mutate( genome )

				leaf.addConnection( genome)
				leaf.addConnection( newGenome)






def  test():
	a = ArtificialPhylogeny()
	for arb in range(5):
		a.evolve()
		print(a.tree)


if __name__ == "__main__":
	test()





