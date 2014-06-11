#/usr/bin/python
from InitializeAnimals import OrdersWrapper
from random import random

def BaseAnimal(Animal,LocalFood):
    Orders=OrdersWrapper()
    
    Orders.Accelerate=0
    Orders.Turn=0
    Orders.Eat=1
    Orders.Reproduce=0
    Orders.Grow=0
    
    
    TotalCost=Animal.Size**.5/1000+Animal.Calories*.01
    TotalGain=min(LocalFood,Animal.Size**.5/100)
    GoalFood=5*(Animal.Size**.5/1000+Animal.Calories*.01)
    CostOfExploring= Animal.Size**.5*(1.0/200+1.0/10+1.0*25.0**2/50000)
    GoalCalories=1.5*CostOfExploring +1.5*TotalCost
    print GoalCalories
    
    GoalCalories=10
    GoalSize=1000
    
    if Animal.Calories>GoalCalories:
        Orders.Grow=(Animal.Calories-GoalCalories)/10
    elif Animal.Calories<GoalCalories/2:
        Orders.Grow=Animal.Calories-GoalCalories/2
        
    if LocalFood<GoalFood and Animal.V==0:
        Orders.Accelerate=1
    elif LocalFood<GoalFood and Animal.V!=0:
        Orders.Turn=25
    elif LocalFood>GoalFood and Animal.V!=0:
        Orders.Accelerate=-1
    
    
    if Animal.Size>2*GoalSize:
        Orders.Reproduce=GoalSize
        Orders.Accelerate=-Animal.V
    

    return Orders
def GetColor():
    return (255,255,0)
## Red, Green, Blue; 255 is the maximum of that color.