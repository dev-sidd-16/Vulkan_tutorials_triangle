#!/usr/bin/env python
from sys import *
import xml.etree.ElementTree as et 
import os

fname = argv[1]

path = os.path.abspath(fname)

file = open(fname, 'r')

content = file.readlines()
count = 0
instance = ''
for line in content:
	tempLine = line.strip()
	instance = instance+line
	#print line
	#raw_input()
	if tempLine == '</nvidia_smi_log>':
		count += 1
		outFName = 'parsed/out'+str(count)+'.xml'
		#tree = et.parse(instance)
		#root = tree.getroot()
		fwr = open(outFName,'w')
		fwr.write(instance)
		fwr.close()
		#print '=====',count,'======'
		#raw_input()
		instance = ''

path = os.path.abspath('parsed')

dirs = os.listdir(path)

print dirs

for directory in dirs:
	newFName = 'parsed/'+directory
	tree = et.parse(newFName)
	root = tree.getroot()
	print newFName
	for child in root:
		if child.tag =='timestamp':
			print child.text
		if child.tag == 'gpu':
			for child1 in child:
				print child1.tag,child1.attrib

	print '======================'
	raw_input()