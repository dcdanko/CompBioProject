


class Genome( object ):

	def __init__( self, genome=None, grimmString="", name="", chromosoneList=[]):

		if genome is not None:
			self.chromosoneList = ogenome.chromosoneList[:]
			self.name = genome.name + "_clone"
		else:
			self.chromosoneList = chromosoneList
			self.name = name

			if grimmString != "":
				if name == "":
					g = grimmString.split("\n")[0]
					if ">" in g:
						self.name = g

				if chromosoneList == []:
					g = self.grimmString.split("\n")
					for line in g:
						if ">" in line or "#" in line:
							pass
						else:
							self.chromosoneList.append([int(val) for val in line if val != "$"])


	def __iter__( self ):
		return iter( self.chromosoneList)

	def __str__( self ):
		grimmString = "> "+self.name+" \n"
		for chromosone in self.chromosoneList:
			for val in chromosone:
				grimmString += str(val) + " "
			grimmString += "$ \n"
		return grimmString

		

	def addChromosone( self, chromosone ):
		if type(chromosone) is str:
			self.chromosoneList.append([int(val) for val in chromosone if val != "$"])

		elif type(chromosone) is list:
			self.chromosoneList.append(chromosone)

		else:
			raise Exception("Unexpected input to add chromosone")

	def getName(self,name=""):
		if name == "":
			return self.name
		else:
			self.name = name
			return self.name
 
