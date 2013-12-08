import StringIO
from tempfile import NamedTemporaryFile
import os
import re

#foo = "Step 1\nStep 2\nStep 3\nStep 999\n"
#foo = "Signs:                          Signed\nNumber of Genomes:              2\nNumber of Genes:                10 + 6 caps\nNumber of Chromosomes:          3\nMultichromosomal Distance:      2\nMultichromosomal Distance:   3\n======================================================================"

#foo = "Multichromosomal Distance:"

#lastidx = foo.rfind('Step')

f = open('sample_GRIMMout.txt','r')
foo = f.read()
f.close()

midstep = 0
pattern = re.compile("Step "+str(midstep)+":(.*?)\n(.*)Step "+str(midstep+1), re.DOTALL)
blah = pattern.search(foo)

#searchObj = re.search(r'Step ([0-9]+)', foo, lastidx)

print blah
print blah.group()
print
print blah.group(1)
print
print blah.group(2)
