#/usr/bin/python

from random import random
from importlib import import_module


class OrdersWrapper():
    def __init__(self):
        self.Accelerate=0
        self.Turn=0
        self.Eat=1
        self.Reproduce=0
        self.Grow=0
        self.Store=0

class AnimalBirthWrapper():
    def __init__(self, Size, Health, Sugar, Fat, Stomach, A):
        self.X=[0,0]
        self.X[0]=A.X[0]
        self.X[1]=A.X[1]
        self.V=0.0
        self.T=A.T
        self.Metabolism=A.Metabolism
        self.Attack=A.Attack
        self.Size=Size
        self.Sugar=Sugar
        self.Fat=Fat
        self.Health=Health
        self.Stomach=Stomach
        self.handle=A.handle
        self.Color=A.Color
        self.Memory=[0 for i in range(len(A.Memory))]
        self.Training=[0 for i in range(len(A.Training))]
        for i in range(len(A.Training)):
            self.Training[i]=A.Training[i]
        

class AnimalWrapper():
	def __init__(self, MyDir, Name, MapSize):
		# Set initial position
		self.X = [random()*MapSize for x in [0,0]]
		# The animal isn't yet moving
		self.V = 0.0
		# Set the initial direction it's facing
		self.T = random()*360.0
		
		print MyDir+Name+".txt"
		
		try:
			frl = open(MyDir + Name + '.txt','r')
			for line in frl:
				if 'Metabolism' == line[:10]:
					self.Metabolism = float(line[10:])
				elif 'Attack' == line[:6]:
					self.Attack = float(line[6:])
				elif 'Size' == line[:4]:
					self.Size = float(line[4:])
			self.Sugar = self.Size/10.0
			self.Fat = self.Size
			#self.Stomach = self.Sugar*100.0/self.Metabolism*0.005
			self.Stomach=0
			self.Health = self.Size
			# Get the function for this animal
			print 'Starting to generate handle'
			temp = import_module(Name, 'pkg.subpkg')
			print 'Finished to generate handle'
			# Setting the function to be called as the handle
			self.handle = getattr(temp, Name)
			print 'here2'
		        self.Color = temp.GetColor()
		        print 'here3'
		        self.Memory = temp.GetMemory()
		        self.Training = temp.GetTraining()
		except:
			print 'Failed to load the parameters for animal {0}'.format(Name)
		
def InitializeAnimals(AnimalReference, MyDir, CurrentAnimals, MapSize):
	Animals = []
	for i in CurrentAnimals:
	    Animals.append(AnimalWrapper(MyDir, AnimalReference[i], MapSize))
	return Animals
		
		
		