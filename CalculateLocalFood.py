#/usr/bin/python

from math import sqrt, ceil, floor
from numpy import mean


def CalculateLocalFood(X, Size, Veg):
	R = Size**.5/80.0
	LocalFood=0
	
	xs=range(int(floor(X[0]-R)),int(ceil(X[0]+R)+1))
	ys=range(int(floor(X[1]-R)),int(ceil(X[1]+R)+1))
	for n1 in range(len(xs)):
	    xs[n1]=xs[n1] % len(Veg)
	for n1 in range(len(ys)):
	    ys[n1]=ys[n1] % len(Veg)
	
	for n1 in xs:
	   for n2 in ys:
	       LocalFood+=Veg[n1][n2]
	LocalFood=LocalFood/(ceil(X[0]+R)-floor(X[0]-R)+1)/(ceil(X[1]+R)-floor(X[1]-R)+1)*R**2*4.0
        return LocalFood