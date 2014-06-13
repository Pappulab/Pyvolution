#/usr/bin/python
from InitializeAnimals import OrdersWrapper
from random import random
from math import acos

def Terminator(Animal,LocalFood):
    Orders=OrdersWrapper()
    Memory=Animal.Memory
    Training=Animal.Training
    
    Orders.Accelerate=0
    Orders.Turn=0
    Orders.Eat=1
    Orders.Reproduce=0
    Orders.Grow=0
    Orders.Store=0
    
    CostOfLife=Animal.Size**.5/1000.0**.5 + Animal.Fat**.5/1000.0**.5
    CostOfSpeed=CostOfLife*2.0
    CostOfAcc=CostOfLife*5.0
    CostOfTurn=CostOfLife*5.0/20**2
    CostOfAttack=CostOfLife
    CostOfSugar=.01
    TotalGain=min(LocalFood,Animal.Size**(.5)/5)
    
    
    
    CostOfExploring= Animal.Size**.5*(1.0/200+1.0/10+1.0*25.0**2/50000)
    GoalSugar=CostOfLife+CostOfSpeed+CostOfTurn*20**2+CostOfAcc
    
    
    
    
    #GoalSugar=10
        
    GoalFood=CostOfLife*3
    if LocalFood<GoalFood/2:
        if Animal.V==0:
            Orders.Accerlate=.5
        
        
    if LocalFood<GoalFood and Animal.V==0: #start a search pattern
        Orders.Accelerate=.5
        Orders.Turn=random()*20-20
    if LocalFood<GoalFood and Animal.V!=0: #continue the search
        if Animal.V==.5 and random()<.3: #if I'm going slow, either stop and turn large, turn small, or speed up
            Orders.Turn=random()*80-40
            Orders.Accelerate=-.5
        elif Animal.V==.5 and random()<.2:
            Orders.Turn=random()*50-25
        elif Animal.V==.5:
            Orders.Accelerate=.5
        if Animal.V==1 and random()<.3: #if I'm going at full speed, maybe I should slow down and turn
            Orders.Turn=random()*50-25
            Orders.Accelerate=-.5
    elif LocalFood>GoalFood and Animal.V!=0:
        Orders.Accelerate=-.5
    
    if Animal.Fat>3000:
        Orders.Reproduce=20
    if Animal.Unborn>1000:
        Orders.Reproduce=-1
        
        
    # My Memory: 
        #0,1,2,3: search pattern alpha time step, location of best food, magnitude of best food, number of search patterns done at this location
        #4: Previous Local Food
    # My Training:
        #0,1,2: Location of best food, Mag of best food

    Training[2]=Training[2]-.02
    if LocalFood>Training[2]:
        Training[2]=LocalFood
        Training[0]=Animal.X[0]
        Training[1]=Animal.X[1]
    
# Search pattern Alpha: ###############
    if Animal.V==1 and Memory[3]>0:
        Memory[3]-=1
    if Memory[3]>0 and random()<.003:
        Memory[3]-=1
#want it to be a .1 chc at M[3]=0, .075 chc at M[3]=1, .05 chac at M[4]=2, .025 at 3, and 0 at 4
    if Animal.Memory[0]==0:
        if LocalFood>GoalFood and Animal.V==0 and random()<.1*(4-Animal.Memory[3]):
            Orders.Accelerate=.6
            Orders.Turn=0
            Memory[0]=1
            Memory[1]=0
            Memory[2]=LocalFood
            Memory[3]+=1
    elif Animal.Memory[0]==1:
        Orders.Accelerate=0
        Orders.Turn=0
        Memory[0]+=1
    elif Animal.Memory[0]==2:
        Orders.Accelerate=-Animal.V+.001
        Orders.Turn=120
        Memory[0]+=1
    elif Animal.Memory[0]==3:
        Orders.Accelerate=.6
        Orders.Turn=0
        if Memory[2]<LocalFood:
            Memory[2]=LocalFood
            Memory[1]=1
        Memory[0]+=1
    elif Animal.Memory[0]==4:
        Orders.Accelerate=0
        Orders.Turn=0
        Memory[0]+=1
    elif Animal.Memory[0]==5:
        Orders.Accelerate=-Animal.V
        if Memory[2]<LocalFood:
            Memory[2]=LocalFood
            Memory[1]=2
        if Memory[1]==2:
            Orders.Turn=-60+random()*60-30
            Memory[0]=0
        else:
            Orders.Turn=120+120*Memory[1]
            Memory[0]=6
    elif Animal.Memory[0]==6:
        Orders.Accelerate=.6
        Orders.Turn=0
        Memory[0]=7
    elif Animal.Memory[0]==7:
        Orders.Accelerate=0
        Orders.Turn=0
        Memory[0]=8
    elif Animal.Memory[0]==8:
        Orders.Accelerate=-Animal.V
        if Animal.Memory[1]==0:
            Orders.Turn=-60+random()*60-30
        else:
            Orders.Turn=0
        #Memory[0]=0
    if Animal.Memory[0]>0:
        a=[Animal.Memory[0],Animal.Memory[1],Animal.Memory[2],Animal.Memory[3],Animal.X[0],Animal.X[1],LocalFood]
        #print ["%0.2f" % i for i in a]
        
    if Animal.Memory[0]==8:
        Memory[0]=0
# End of search pattern Alpha ###############
    
# Store Local Food and stuff:
    Memory[4]=LocalFood
    
        
        
    
    GoalSize=1000
    if Animal.Sugar>GoalSugar:
        Orders.Store=(Animal.Sugar-GoalSugar)/2
    elif Animal.Sugar<GoalSugar:
        Orders.Grow=Animal.Sugar-GoalSugar
    
    
    
    return [Orders,Memory,Training]
def GetColor():
    return (0,0,0)
## Red, Green, Blue; 255 is the maximum of that color.
def GetMemory():
    return [0,0,0,0,0,0,0,0,0,0,0,0]
def GetTraining():
    return [0,0,0,0,0,0,0,0,0,0,0,0]