#/usr/bin/python

#def start():
temp=True
if temp:
    
    from InitializeAnimals import *
    from InitializePlants  import *
    from SingleAnimalOrders import *
    from CalculateLocalFood import *
    from AnimalsRun import *
    from random import random, seed
    
    # Directory:
    MyDir="/Users/tylerharmon/Documents/Outreach/PythonVersion/"
    seed(12)
    
    # All animals that are known
    AnimalReference = ['BaseAnimal']
    # Animals currently in the trial
    CurrentAnimals = [0,0,0,0,0,0]
    # Initialize all animals in args as 'alive'
    Alive = [True for x in range(len(CurrentAnimals))]
    MapSize = 20
    Animals = InitializeAnimals(AnimalReference, MyDir, CurrentAnimals, MapSize)
    Veg_G1 = InitializePlants(MapSize, 10)
    Veg_G2 = InitializePlants(MapSize, 10)
    Veg_D  = InitializePlants(MapSize, 10)
    Veg = InitializePlants(MapSize, 100)
    Or = [[0 for x in range(6)] for y in range(50)]
    
    # Acceleration, Turn, Eat, Reproduce, Grow
    for t in range(10000):
        if (t % 100)==0:
            print t
            print Animals[0].X
        
        for i in range(len(Alive)):
            if Alive[i]:
                SingleAnimalOrders(Animals,i,Veg,Or)
        AnimalsRun(Animals,CurrentAnimals,Alive,Or)
        
    exit()














