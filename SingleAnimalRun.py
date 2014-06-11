
from math import sin, cos


def AnimalsRun(Animals,Alive,Or):
    
    for i in range(len(Alive)):
        Animals[i].V+=Or[i][0]
        Animals[i].T+=Or[i][1]
        Animals[i].X[0]+=
        
        
    #Or[i][0]=Orders.Accelerate
    #Or[i][1]=Orders.Turn
    #Or[i][2]=Orders.Eat
    #Or[i][3]=Orders.Reproduce
    #Or[i][4]=Orders.Grow