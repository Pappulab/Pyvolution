#/usr/bin/python

import time
import threading

from InitializeAnimals import *
from InitializePlants  import *
from SingleAnimalOrders import *
from CalculateLocalFood import *
from AnimalsRun import *
from random import random, seed
from math import log
    

def threadSimulation_Mixed(gui):
	timesteps = 50000
        seed(120)
        # Directory:
        MyDir="/Users/tylerharmon/Documents/Outreach/PythonVersion/"
        
        # All animals that are known
        AnimalReference = ['Terminator']
        # Animals currently in the trial
        CurrentAnimals = [0]
        # Initialize all animals in args as 'alive'
        Alive = [True for x in range(len(CurrentAnimals))]
        MapSize = 50
        Animals = InitializeAnimals(AnimalReference, MyDir, CurrentAnimals, MapSize)
        
        PrintSize = [a.Size**.5/30/MapSize for a in Animals]
        PrintTheta = [180.0-a.T for a in Animals]
	PrintColor = [a.Color for a in Animals]
	PrintOldX = [[(a.X[0]+.5)/MapSize, (a.X[1]+.5)/MapSize] for a in Animals]
	
	
	
        Veg_G1 = InitializePlants(MapSize, 0)
        Veg_G1=[[Veg_G1[j][k]/500+5 for k in range(MapSize)] for j in range(MapSize)]
        Veg_G2 = InitializePlants(MapSize, 0)
        Veg_G2=[[Veg_G2[j][k]/100 for k in range(MapSize)] for j in range(MapSize)]
        Veg_D  = InitializePlants(MapSize, 0)
        Veg_D=[[Veg_D[j][k]/150+.001 for k in range(MapSize)] for j in range(MapSize)]
        Veg = InitializePlants(MapSize, 0)
        PrintVeg=[[0 for k in range(MapSize)] for j in range(MapSize)]
        Veg_Max=[[Veg_G1[j][k]+ (1+Veg_G2[j][k])**2/Veg_D[j][k]/4 for k in range(MapSize)] for j in range(MapSize)]
        VegM=0
        for j in range(MapSize):
            for k in range(MapSize):
                if Veg[j][k]>VegM:
                    VegM=Veg[j][k]
                if Veg_G1[j][k]+ (1+Veg_G2[j][k])**2/Veg_D[j][k]/4>VegM:
                    VegM=Veg_G1[j][k]+ (1+Veg_G2[j][k])**2/Veg_D[j][k]/4
        MaxColor=1
        LinVeg=10.0
        for j in range(MapSize):
            for k in range(MapSize):
                if Veg[j][k]<= LinVeg:
                    PrintVeg[j][k]= Veg[j][k]/LinVeg/2.0
                else:
                    PrintVeg[j][k]= (log(Veg[j][k]/VegM) + log(VegM/LinVeg))/log(VegM/LinVeg)/2 + .5
		           
        
	gui.queue.put(['initializePlants',PrintVeg, 1])  ## change the one to the max plant size
	gui.queue.put(['initializeAnimals',PrintColor, PrintSize, PrintOldX, PrintTheta]) 
	Or = [[0 for x in range(6)] for y in range(len(CurrentAnimals))]
        
        
	start = time.time()
	previous = int(start)
	end = time.time()
	canceled = False
	lock = threading.Lock()
	lock.acquire()
	try:
		sp = gui.speed.get()
	except:
		sp = 1000 #default
	finally:
		lock.release()
	
	for i in range(timesteps):
		# pause if the user specified pause
		gui.runEvent.wait()
		
		lock.acquire()
		try:
			sp = gui.speed.get()
			canceled = gui.canceled
		finally:
			lock.release()
		
		# cancel if the user wants to cancel
		if canceled:
			break
		
		start = time.time()
                #gui.queue.put(str(i))
		
# If no one is alive, end the program: ###########################################
		#if not any(Alive):
		    #gui.queue.put('Everyone is Dead!')
		    #gui.queue.put(['cancel'])
		
# Start of Real Simulation: ##########################################################################
		
                for i2 in range(len(Alive)):
                    if Alive[i2]:
                        SingleAnimalOrders(Animals,i2,Veg,Or,gui)
                AnimalsRun(Animals,CurrentAnimals,Alive,Or,MapSize,gui,i)
		
		
		if random()<1.0:
		    for j in range(MapSize):
		        for k in range(MapSize):
		           Veg[k][j]+= Veg_G1[k][j]+Veg[k][j]*Veg_G2[k][j] - Veg_D[k][j]*Veg[k][j]**2
		           Veg[k][j]= 0 if Veg[k][j]<0 else Veg[k][j]
		           
#Finished calling a simulation step here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		gui.queue.put(str(Veg[1][1]))

		if i % 100 ==1:
                    #gui.queue.put(str([i,len(Alive),int(Animals[0].V),int(Animals[0].T),int(Animals[0].Size),int(Animals[0].Calories),int(Animals[0].Stomach),Animals[0].Memory[1]]))
                    gui.queue.put(str(Veg[1][1]))
		
# My Print Statement Ends HERE::::##########################                    
                
		if (int(time.time()) != previous) or i+1==timesteps:
                        PrintSize = [a.Size**.5/30/MapSize for a in Animals]
                        PrintTheta = [180.0-a.T for a in Animals]
       	                PrintNewX = [[(a.X[0]+.5)/MapSize, (a.X[1]+.5)/MapSize] for a in Animals]
	                
	                #gui.queue.put(str(PrintDeltaX))
	                
			# Request that the GUI run one of its own functions
##############################
                        MaxColor=1
                        for j in range(MapSize):
                            for k in range(MapSize):
                                if Veg[j][k]<= LinVeg:
                                    PrintVeg[j][k]= Veg[j][k]/LinVeg/2.0
                                else:
                                    PrintVeg[j][k]= (log(Veg[j][k]/VegM) + log(VegM/LinVeg))/log(VegM/LinVeg)/2 + .5
                        
			gui.queue.put(['updatePlants',PrintVeg, MaxColor])  # Replace 1 with the maximum food
###############################   delta(X,Y) position :::: Theta
			gui.queue.put(['updateAnimals',Alive, PrintSize, PrintNewX, PrintTheta])
			#gui.queue.put('Output at timestep: ' + str(i+1) + '/' + str(timesteps))
			previous = int(time.time())
		end = time.time()
		
		# Account for the time it took to actually perform the simulation step
		curTime = end - start
		
		# This makes the response more immediate/dynamic during user interaction
		while curTime < sp:
			# pause if the user specified pause
			gui.runEvent.wait()
			# Find the true starting time
			start = time.time()
			# Sleep for a little
			time.sleep(.01 if (sp-curTime)/.01 > 1 else (sp-curTime)%.01)
			# Check the speed on the GUI
			lock.acquire()
			try:
				sp = gui.speed.get()
				canceled = gui.canceled
			finally:
				lock.release()
			# cancel if appropriate
			if canceled:
				break
			# Add the true increase in time
			curTime += (time.time()-start)*1000
			
		#if not canceled:
		#	gui.queue.put('Performed time step ' + str(i+1) + ' after ' + '%.2f'%curTime + ' milliseconds')