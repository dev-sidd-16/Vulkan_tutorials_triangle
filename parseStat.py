#!/usr/bin/env python
from sys import *
import xml.etree.ElementTree as et 
import os

fname = argv[1]

path = os.path.abspath(fname)

file = open(fname, 'r')

content = file.readlines()
count = 1
while line in content:
	print line, 

