#!/usr/bin/env python
from sys import *
import xml.etree.ElementTree as et 
import os
import numpy as np
import matplotlib.pyplot as plt
import pylab

fname = argv[1]
# path = os.path.abspath('parsed')
# dirs = os.listdir(path)
# path = path +'/*.xml'
# print path
# if len(dirs) >0:
# 	os.remove(path)
#
# exit(0)
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

dirs.sort()
times = np.zeros(len(dirs))
memory = np.zeros(len(dirs))
tx = np.zeros(len(dirs))
rx = np.zeros(len(dirs))
clock = np.zeros(len(dirs))
print times
print memory

for directory in dirs:
	newFName = 'parsed/'+directory
	tree = et.parse(newFName)
	root = tree.getroot()
	print newFName
	pa = os.path.abspath(newFName)
	name = os.path.basename(pa)
	name = name.split('.')[0]
	time = int(name[3:])
	times[time-1] = time
	#print 'time:',time
	#print 'memory:',memory
	for child in root:
		if child.tag =='timestamp':
			print child.text
		if child.tag == 'gpu':
			for child1 in child:
				#print child1.tag,child1.attrib
				if child1.tag == 'pci':
					for child2 in child1.findall('tx_util'):
						#print 'TX Throughput:', child2.text
						tem = float(child2.text.split()[0])
						tx[time-1] = tem
					for child2 in child1.findall('rx_util'):
						#print 'RX Throughput:', child2.text
						rem = float(child2.text.split()[0])
						rx[time-1] = rem
				if child1.tag == 'fb_memory_usage':
					for child2 in child1.findall('used'):
						#print 'Total FB Memoru used:',child2.text
						mem = float(child2.text.split()[0])
						memory[time-1] = mem
				if child1.tag == 'clocks':
					for child2 in child1.findall('graphics_clock'):
						#print 'Graphics Clock:', child2.text
						cl = float(child2.text.split()[0])
						clock[time-1] = cl

	
	print '======================'
	#raw_input()

fig = plt.figure()
print times,memory
fig = plt.plot(times,memory)
plt.ylabel('MiB')
plt.xlabel('sec')
plt.title('FB Memory Usage')
plt.show()
#fig[0].savefig('memory.pdf')

print times,tx
fig = plt.plot(times,tx)
plt.ylabel('KB/sec')
plt.xlabel('sec')
plt.title('TX Throughput')
plt.show()
#fig[0].savefig('tx.pdf')

print times,rx
fig = plt.plot(times,rx)
plt.ylabel('KB/sec')
plt.xlabel('sec')
plt.title('RX Throughput')
plt.show()
#fig[0].savefig('rx.pdf')

print times,clock
fig = plt.plot(times,clock)
plt.ylabel('MHz')
plt.xlabel('sec')
plt.title('Clock Frequency')
plt.show()
#fig[0].savefig('clock.pdf')