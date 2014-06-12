#/usr/bin/python

from random import random
from math import exp, ceil

def InitializePlants(MapSize, patches, multipatch):
	Veg = [[0 for x in range(MapSize)] for y in range(MapSize)]
	for n in range(patches):
		R = [random()*x for x in [MapSize, MapSize, 10, 40]]
		d = min(MapSize, int(ceil(R[2]*3)))
		for i in range(-d, d+1):
			for j in range(-d, d+1):
				Veg[int((i + round(R[0]))%MapSize)][int((j + round(R[1]))%MapSize)] += R[3]*exp(-1.0/R[2]*(pow(i + 1 + round(R[0])-R[0],2) + pow(j + 1 + round(R[1])-R[1],2)))
		for m in range(multipatch):
		    R2 = [random()*x for x in [2*R[2],2*R[2],2*R[2],2*R[3]]]
		    R2[0] += R[0]
		    R2[1] += R[1]
		    d = min(MapSize, int(ceil(R2[2]*3)))
		    for i in range(-d, d+1):
			for j in range(-d, d+1):
				Veg[int((i + round(R2[0]))%MapSize)][int((j + round(R2[1]))%MapSize)] += R2[3]*exp(-1.0/R2[2]*(pow(i + 1 + round(R2[0])-R2[0],2) + pow(j + 1 + round(R2[1])-R2[1],2)))
	return Veg