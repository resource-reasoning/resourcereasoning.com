#!/usr/bin/python
import sys
import re

def increpl(match):
	incfile = open(match.groups()[0], 'r')
	subst = incfile.read()
	incfile.close()
	return subst

infile = open(sys.argv[1], 'r')
indata = infile.read()
infile.close()
outfile = open(sys.argv[2], 'w')
outdata = re.sub('<!--#include\s+virtual="([^"]*)"\s*-->', increpl, indata)
outfile.write(outdata)
outfile.close()

