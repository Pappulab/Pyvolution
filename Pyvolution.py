#/usr/bin/python

from Tkinter import *
from operator import add

import threading
import Queue
from math import sin, cos, pi

from threadSimulation_Mixed import *		# Arbitrary simulation skeleton

class ScaleSpeed():
    def __init__(self):
        self.value = 0
    def set(self, val):
        self.value = val
    def scalePow(self, val):
        self.value = int(10**(float(val)/10000.0))
    def get(self):
        return self.value

class Pyvolution(Frame):
	def __init__(self, gridSize=20, master=None):
		Frame.__init__(self, master)
		self.master.title('Pyvolution')
		self.grid(sticky=N+S+E+W)
		self.plantIDs = []
		self.animalIDs = []
		self.animalColors = []
		self.deadIDs = []
		self.usingLoad = False
		self.speed = ScaleSpeed()
		self.height = 700
		self.width = 700
		self.__createWidgets__()
		
		self.runEvent = threading.Event()
		self.canceled = False
		self.queue = Queue.Queue()
		
		
	def __createWidgets__(self):
	   
		self.canvas = Canvas(self,  height=self.height,  width=self.width)
		self.canvas.grid(row=1, column=0,  columnspan=10, sticky=E+W)
		
		self.scaleLabel = Label(self, text="Simulation Speed", padx=0)
		self.scaleLabel.grid(row=4, column=0)
		
		self.scaleWidget = Scale(self,  from_=30000,  to=0,  orient=HORIZONTAL,
		command=self.speed.scalePow,  showvalue=0)
		self.scaleWidget.set(15000)
		self.scaleWidget.grid(row=4,  column=1, columnspan=7,  sticky=W+E)
		
		# Buttons that are active when there is no simulation running
		self.quitButton = Button(self, text='Quit',  command=self.quit,  fg='red')
		self.quitButton.grid(row=4,  column=9,  sticky=E)
		
		self.loadButton = Button(self, text='Load', command=self.load, fg='green')
		self.loadButton.grid(row=4, column=9, sticky=W)
		
		self.simButton = Button(self, text='Simulate', command=self.simulate, fg='blue')
		self.simButton.grid(row=4, column=8, sticky=W+E)
		
		# Buttons that are only visible when the simulation is running
		self.cancelButton = Button(self, text='Cancel', command=self.cancel, fg='red')
		self.cancelButton.grid(row=4, column=9, sticky=E)
		self.cancelButton.grid_remove()
		
		self.pauseButton = Button(self, text='Pause', command=self.pause, fg='dark goldenrod')
		self.pauseButton.grid(row=4, column=9, sticky=W)
		self.pauseButton.grid_remove()
		
		# Continue will only be visible after pause is selected
		self.continueButton = Button(self, text='Continue', command=self.cont, fg='green')
		self.continueButton.grid(row=4, column=9, sticky=W)
		self.continueButton.grid_remove()
		
	
	def initializePlants(self, plantSizes, maxCal):
		'''
		Initialize the plants in the grid.
		plantSizes is a matrix giving the caloric value of each plant
		maxCal gives the theoretical maximum amount of calories any plant can have on the grid
		'''
		print 'Initialize Plants'
		self.plantIDs = []
		
		gridSizeX = len(plantSizes)
		gridSizeY = len(plantSizes[0])
		
		# These are the RG values of the extremes
		# Blue is always 6
		dirt = (143, 95)
		lush = (19, 79)
		
		# For each position in the grid
		for i in range(gridSizeX):
			objID = []
			for j in range(gridSizeY):
				# Find the percentage of maximum growth for this plant
				pPlant = float(plantSizes[i][j])/float(maxCal)
				# Mix dirt and lush accordingly
				tupColor = tuple([int(a) for a in map(add, [d*(1-pPlant) for d in dirt], [l*pPlant for l in lush])] + [6])
				# Format the color to hex
				thisColor = '#%02x%02x%02x' % tupColor
				# Set the grid location to this color
				oneID = self.canvas.create_rectangle(
				i*self.canvas.winfo_width()/gridSizeX, 
				j*self.canvas.winfo_height()/gridSizeY,
				(i+1)*self.canvas.winfo_width()/gridSizeX, 
				(j+1)*self.canvas.winfo_height()/gridSizeY, 
				fill= thisColor)
				
				objID.append(oneID)
			self.plantIDs.append(objID)
		print 'Initialized plants ' , str(len(self.plantIDs))
				
	def updatePlants(self, plantSizes, maxCal):
		'''
		Updates the plants on the grid to their new caloric levels
		'''
		gridSizeX = len(plantSizes)
		gridSizeY = len(plantSizes[0])
		
		# These are the RG values of the extremes
		# Blue is always 6
		dirt = (143, 95)
		lush = (19, 79)
		
		# For each position in the grid
		for i in range(gridSizeX):
			for j in range(gridSizeY):
				# Find the percentage of maximum growth for this plant
				pPlant = float(plantSizes[i][j])/float(maxCal)
				# Mix dirt and lush accordingly
				tupColor = tuple([int(a) for a in map(add, [d*(1-pPlant) for d in dirt], [l*pPlant for l in lush])] + [6])
				# Format the color to hex
				thisColor = '#%02x%02x%02x' % tupColor
				# Update the grid location to this color
				self.canvas.itemconfig(self.plantIDs[i][j], fill=thisColor)
				
	
	def initializeAnimals(self, colorArr, sizeArr, posArr, rotArr):
		'''
		Initializes the animals on the grid
		colorArr is a list of RGB tuples
		sizeArr has the starting size of each animal
		posArr has the starting position where (0,0) is the top, right corner
		rotArr has the starting rotation direction in degrees
		'''
		
		# Save this list for reference
		self.animalColors += colorArr
		
		# The angle of the animal arc
		angle = 40
		
		if len(colorArr) == len(sizeArr) == len(posArr):
			for i in range(len(colorArr)):
			        R=sizeArr[i]*self.width
				anID = self.canvas.create_arc(
				-R - 2.0/3.0*R*cos((rotArr[i]+20.0)/180.0*pi) + posArr[i][0]*self.width,
				-R + 2.0/3.0*R*sin((rotArr[i]-20.0)/180.0*pi) + posArr[i][1]*self.width,
				R - 2.0/3.0*R*cos((rotArr[i]+20.0)/180.0*pi) + posArr[i][0]*self.width,
				R + 2.0/3.0*R*sin((rotArr[i]-20.0)/180.0*pi) + posArr[i][1]*self.width,
				fill='#%02x%02x%02x' % colorArr[i],
				extent=angle,
				start=rotArr[i]-20)
				
				self.animalIDs.append(anID)
		else:
			raise ValueError('All lists must have the same number of animals')
	
	def updateAnimals(self, isAliveArr, sizeArr, posArr, rotArr):
		'''
		Updates the animals on the grid
		isAliveArr is an array of booleans as to whether each animal is alive or not
		dSizeArr is the change in size of an animal
		dPosArr is the change in position of an animal (tuples/lists of (x,y))
		rotArr gives the direction (in degrees) that the animal is facing
		'''
		if len(self.animalIDs) == len(isAliveArr) == len(sizeArr) == len(posArr) == len(rotArr):
			for i in range(len(self.animalIDs)):
				# Rotate each animal
				self.canvas.itemconfig(self.animalIDs[i], start=rotArr[i]-20)
				# Resize the object 
				# Note: the reference point is the top-left of the object so the object may shift on resizing
				#	This is accounted for by shifting the starting point back
			        R=sizeArr[i]*self.width
				self.canvas.coords(self.animalIDs[i],
				-R - 2.0/3.0*R*cos((rotArr[i]+20.0)/180.0*pi) + (posArr[i][0])*self.width,
				-R + 2.0/3.0*R*sin((rotArr[i]-20.0)/180.0*pi) + (posArr[i][1])*self.width,
				R - 2.0/3.0*R*cos((rotArr[i]+20.0)/180.0*pi) + (posArr[i][0])*self.width,
				R + 2.0/3.0*R*sin((rotArr[i]-20.0)/180.0*pi) + (posArr[i][1])*self.width)
				
		else:
			raise ValueError('All lists must have the same number of animals\n' + 
			'len(animalIDs)=' + str(len(self.animalIDs)) +
			'len(isAliveArr)=' + str(len(isAliveArr)) +
			'len(sizeArr)=' + str(len(sizeArr)) +
			'len(posArr)=' + str(len(posArr)) +
			'len(rotArr)=' + str(len(rotArr)))
	
	def kill(self, index):
		'''
		Kills an animal and replaces its object with a cross
		'''
		# Get the coordinates of the animal that died
		coords = self.canvas.coords(self.animalIDs[index])
		# Delete the animal from the grid
		self.canvas.delete(self.animalIDs[index])
		# Find the center of the arc object
		center = ((coords[0]+coords[2])/2, (coords[1]+coords[3])/2)
		# Put an X at that location
		c1 = self.canvas.create_line(center[0]-5, center[1]-5, center[0]+5, center[1]+5, fill='#%02x%02x%02x' % self.animalColors[index], width=2)
		c2 = self.canvas.create_line(center[0]+5, center[1]-5, center[0]-5, center[1]+5, fill='#%02x%02x%02x' % self.animalColors[index], width=2)
		# Store the deadIDs for reference
		self.deadIDs.append((c1,c2))
	
	def simulate(self):
		import time
	
		# Hide: sim/quit and Show: pause/cancel
		self.pauseButton.grid()
		self.cancelButton.grid()
		self.simButton.grid_remove()
		self.loadButton.grid_remove()
		self.quitButton.grid_remove()
		
		self.scaleWidget.grid(columnspan=8)
		
		self.canceled = False
		# Kill everything
		self.canvas.delete(ALL)
		
		self.animalIDs = []
		self.deadIDs = []
		self.plantIDs = []
		
		# If this is the first simulation that the user is running on this instance...
	        thread1 = threading.Thread(target=threadSimulation_Mixed, args=(self,))
	        thread1.setDaemon(True)
		thread1.start()
		
		self.runEvent.set()
		print 'start'
		# While the simulation thread is executing the simulation
		while thread1.isAlive():
			start = time.time()
			# Check the queue to see if anything new has been added
			while not self.queue.empty():
				response = self.queue.get()
				if isinstance(response, basestring):
					print str(response)
				elif isinstance(response, list):
					aFunc = getattr(self, response[0])
					aFunc(*tuple(response[1:]))
			self.update()
			runTime = time.time() - start
			
			# Wait 10 milliseconds (Max FPS: 100)
			if runTime < .01:
				time.sleep(.01 - runTime)
		
		print 'end'
		thread1.join()
		
		# Show: sim/quit and Hide: pause/cancel
		self.pauseButton.grid_remove()
		self.cancelButton.grid_remove()
		self.simButton.grid()
		self.loadButton.grid()
		self.quitButton.grid()
		
		self.scaleWidget.grid(columnspan=7)
	
	def load(self):
	    self.usingLoad = True
	    self.simulate()
			
	def pause(self):
		self.pauseButton.grid_remove()
		self.continueButton.grid()
		# Block the simulation thread until cont() is called 
		self.runEvent.clear()
		# Can't cancel if the thread is blocked
		self.cancelButton.config(state='disabled')
		
	def cont(self):
		self.continueButton.grid_remove()
		self.pauseButton.grid()
		self.runEvent.set()
		# Now that the thread isn't blocked, it can be canceled
		self.cancelButton.config(state='normal')
	
	def cancel(self):
		lock = threading.Lock()
		lock.acquire()
		try:
			self.canceled = True
		finally:
			lock.release()
		
		
	def getSpeed(self):
		return self.speed.get()
		
	
		
if __name__ == '__main__':
	root = Tk()
	app = Pyvolution(master=root)
	app.mainloop()
	root.destroy()