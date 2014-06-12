#/usr/bin/python
from InitializeAnimals import OrdersWrapper
from random import random
from math import acos

def BaseAnimal(Animal,LocalFood):
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
    
    GoalFood=CostOfLife*1.5
    if LocalFood<GoalFood/2:
        if Animal.V==0:
            Orders.Accelerate=.5
    
    
    
    GoalSugar=CostOfLife
    GoalSugar+= (Orders.Accelerate**2*CostOfAcc + (Orders.Accelerate+Animal.V)*CostOfSpeed
    + Orders.Turn**2*CostOfTurn + Orders.Reproduce)
    GoalSugar=GoalSugar/.98
    if Animal.Sugar>GoalSugar:
        Orders.Store=(Animal.Sugar-GoalSugar)
    elif Animal.Sugar<GoalSugar:
        Orders.Store=Animal.Sugar-GoalSugar
    
    
    #print 'GoalSugar'
    #print GoalSugar
    #print LocalFood
    #print [Animal.Size,Animal.Stomach,Animal.Sugar]
    
    return [Orders,Memory,Training]
def GetColor():
    return (0,0,0)
## Red, Green, Blue; 255 is the maximum of that color.
def GetMemory():
    return [0,0,0,0,0,0,0,0,0,0,0,0]
def GetTraining():
    return [0,0,0,0,0,0,0,0,0,0,0,0]