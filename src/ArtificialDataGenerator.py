import random as rn
from genome import Genome
from Tree import Tree

class ArtificialPhylogeny( object ):


	def __init__( self, size=5, numChromosomes=3):
		self.original = Genome(name="origin")
		for c in range( numChromosomes ):
			self.original.addChromosome(range( c*size+1, (c+1)*size+1 ))

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

		def reversal( ancestor ):
			n = ancestor.getName()
			ancestor.getName(name=n+"_Rev")
			chromosome = rn.choice(ancestor.chromosomeList)
			if len(chromosome) == 0:
				print(ancestor)
				assert False
			start = rn.randrange(len(chromosome))
			end = rn.randrange( start, len(chromosome))
			a,b,c = chromosome[:start], chromosome[start:end:], chromosome[end:]
			b = [-1*val for val in b]
			b = b[::-1]
			revChromosome = a + b + c
			assert len(revChromosome) == len(chromosome)
			ind = ancestor.chromosomeList.index(chromosome)
			ancestor.chromosomeList[ind] = revChromosome
	
		def translocate( ancestor ):
			n = ancestor.getName()
			ancestor.getName(name=n+"_Trans")
			(chrA, chrB) = rn.sample(ancestor.chromosomeList,2)
			stA,stB = rn.randint(0, len(chrA)), rn.randint(0, len(chrB))
			enA,enB = rn.randint(stA,len(chrA)), rn.randint(stB,len(chrB))

			transA= [a for i, a in enumerate(chrA) if i >= stA and i <=enA]
			if rn.random() < 0.5:
				transA = transA[::-1]
				transA = [-val for val in transA]

			transB= [b for i, b in enumerate(chrB) if i >= stB and i <=enB]
			if rn.random() < 0.5:
				transB = transB[::-1]
				transB = [-val for val in transB]

			frontA, backA, frontB, backB = chrA[:stA], chrA[enA+1:], chrB[:stB], chrB[enB+1:]
			tempA, tempB = frontA+transB+backA, frontB+transA+backB

			aInd = ancestor.chromosomeList.index(chrA)
			if len(tempA) > 0:
				ancestor.chromosomeList[aInd] = tempA
			else:
				ancestor.chromosomeList.pop(aInd)

			bInd = ancestor.chromosomeList.index(chrB)
			if len(tempB) > 0:
				ancestor.chromosomeList[bInd] = tempB
			else:
				ancestor.chromosomeList.pop(bInd)

		def split( ancestor):
			n = ancestor.getName()
			ancestor.getName(name=n+"_Split")
			chromosome = rn.choice(ancestor.chromosomeList)
			i = rn.randrange(1,len(chromosome))
			a,b = chromosome[:i], chromosome[i:]
			k = ancestor.chromosomeList.index( chromosome)
			ancestor.chromosomeList[k] = a
			ancestor.chromosomeList.append(b)


		if mod == "REVERSAL":
			reversal( ancestor )


		elif mod == "TRANSLOCATION":
			if len(ancestor.chromosomeList) > 1 and rn.random > 0.1:
				translocate( ancestor )
			else:
				split( ancestor )
					

		return ancestor

	def evolve(self, evolutionRate=0.5):
		for tip in  self.tree.getTips():
			if rn.random() < evolutionRate:
				newGenome = Genome( genome=tip.genome )
				self.mutate( newGenome )

				if rn.random() < evolutionRate:
					self.mutate( tip.genome )

				tip.addConnection( tip.genome)
				tip.addConnection( newGenome)






def  test():
	a = ArtificialPhylogeny()
	for arb in range(10):
		a.evolve()
		print(a.tree)


if __name__ == "__main__":
	test()





