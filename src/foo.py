import StringIO
from tempfile import NamedTemporaryFile
import os

foo = "a\nb\nc\nd\ne\n"

f = NamedTemporaryFile()
f.write(foo)
f.seek(0)

line = f.read()
print "line: "+line


#line = buf.readline()
#while(line):
#	print type(line)
#	print line[-1]
#	print line
#	line = buf.readline()

