import testupgma
import testnobranchupgma

import sys

def parseDistMatrix(grimmfile):

  f = open(grimmfile, 'r')
  output = f.read()
  distMatrix = output.partition('Distance Matrix:')[2]
  distMatrix = distMatrix.strip()

  splitStr = distMatrix.split("\n")

  numGenomes = int(splitStr[0])
  genomes = [0 for x in xrange(numGenomes)] 
  distArray = [ [0 for x in xrange(numGenomes)] for x in xrange(numGenomes)]
  for x in xrange(1, len(splitStr)):
    splitMatrix = splitStr[x].split()
    genomes[x-1] = splitMatrix[0]
    for y in xrange(1, len(splitMatrix)):
      distArray[x-1][y-1] = float(splitMatrix[y]) 

  return (genomes, distArray)

def main():
  if len(sys.argv) < 1:
    print "you must call this program as: "
    print "    python upgma.py <GRIMM output file>"

  grimmfile = sys.argv[1]
  (genomes, distArray) = parseDistMatrix(grimmfile)
#  clu = testupgma.make_clusters(genomes)
#  tree = testupgma.regroup(clu, distArray)
#  testupgma.pprint(tree, tree.height)
  clu = testnobranchupgma.make_clusters(genomes)
  tree = testnobranchupgma.regroup(clu, distArray)
  testnobranchupgma.pprint(tree, tree.height)

  print
  repeatedUPGMApairs(tree)

def repeatedUPGMApairs(upgma):
        #leaf
        if upgma.size == 1:
                return upgma.data
        else:
                left_subtree = repeatedUPGMApairs(upgma.data[0])
                right_subtree = repeatedUPGMApairs(upgma.data[1])
                print "left: "+str(left_subtree)
                print "right: "+str(right_subtree)
		return str(left_subtree)+", "+str(right_subtree)

main()
