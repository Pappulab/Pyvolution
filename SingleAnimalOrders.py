
from CalculateLocalFood import *
from EatLocalFood import *

def SingleAnimalOrders(Animals,i,Veg,Or,gui):
    
    LocalFood=CalculateLocalFood(Animals[i].X,Animals[i].Size,Veg)
    [Orders,Memory,Training]=Animals[i].handle(Animals[i],LocalFood)
    Animals[i].Memory=Memory
    Animals[i].Training=Training
    
    #fixes any stupid orders
    if Orders.Accelerate+Animals[i].V<=0:
        Orders.Accelerate=-Animals[i].V
    elif Orders.Accelerate+Animals[i].V>0:
        Orders.Eat=0
        Orders.Reproduce=0
    if Orders.Reproduce<0:
        Orders.Reproduce=0
    Orders.Turn=(Orders.Turn +180 % 360) - 180
    Orders.Attack=0
    
    CostOfLife=(Animals[i].Size + Animals[i].Fat)**.5/1000.0**.5
    CostOfSpeed=CostOfLife
    CostOfAcc=CostOfLife*4.0
    CostOfTurn=CostOfLife/20**2
    CostOfAttack=CostOfLife
    CostOfSugar=.01
    
    
    Eat=Orders.Eat*min(LocalFood/10,min(LocalFood/10,Animals[i].Size/100))
    Eat=Orders.Eat*min(LocalFood,Animals[i].Size**(.5)/5)
    if Orders.Eat>0 and Eat>0:
        #gui.queue.put(str(Eat))
        EatLocalFood(Animals[i].X, Animals[i].Size, Veg, Eat)
        
    Animals[i].Stomach+= Eat - Animals[i].Stomach*Animals[i].Metabolism/100
    
    #pay the caloires:
    Animals[i].Sugar+= (- CostOfLife 
    - CostOfSugar*Animals[i].Sugar + 
    Animals[i].Metabolism*(1-Animals[i].Metabolism)/100*Animals[i].Stomach - 
    Orders.Grow - Orders.Store - Orders.Reproduce - CostOfSpeed*(Animals[i].V+Orders.Accelerate) - 
    CostOfAcc*Orders.Accelerate**2 - CostOfTurn*(Animals[i].V+Orders.Accelerate)*Orders.Turn**2 - 
    CostOfAttack*Orders.Attack)
    
    Or[i][0]=Orders.Accelerate
    Or[i][1]=Orders.Turn
    Or[i][2]=Orders.Attack
    Or[i][3]=Orders.Reproduce
    Or[i][4]=Orders.Grow
    Or[i][5]=Orders.Store
    print Or[0]
    
