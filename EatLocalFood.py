#/usr/bin/python

from math import sqrt
from math import ceil, floor

def EatLocalFood(X, Size, Veg, Eat):
    R=Size**.5/80
    
    xs=range(int(floor(X[0]-R)),int(ceil(X[0]+R)+1))
    ys=range(int(floor(X[1]-R)),int(ceil(X[1]+R)+1))
    Dist = [[0.0 for x in range(3)] for y in range(len(xs)*len(ys))]
    SumVegPDist = 0
    n=0
    
    for i0 in range(len(xs)):
        for i1 in range(len(ys)):
            Dist[n][0]=sqrt(float(xs[i0]-X[0])**2+float(ys[i1]-X[1])**2)
            Dist[n][1]=xs[i0] % len(Veg)
            Dist[n][2]=ys[i1] % len(Veg)
            n+=1
    
    #print 'h'
    #print Dist
    #print 'h2'
    #print sorted(Dist)
    #DistS=sorted(Dist)
    #
    
    
    for n in range(len(Dist)):
        EatF=min(Eat,Veg[Dist[n][1]][Dist[n][2]])
        Veg[Dist[n][1]][Dist[n][2]]-=EatF
        Eat-=EatF
        if Veg[Dist[n][1]][Dist[n][2]]<-0.1:
            print 'Negative Food!'
            print Veg[Dist[n][1]][Dist[n][2]]
    return Veg