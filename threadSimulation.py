#/usr/bin/python

import time
import threading

from random import random

def threadSimulation(gui):
	start = time.time()
	previous = int(start)
	end = time.time()
	canceled = False
	timesteps = 100000
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
		# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!call a simulation step here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		# Place holder for simulation
		time.sleep(.005)
		if (int(time.time()) != previous) or i+1==timesteps:
			# Request that the GUI run one of its own functions
			gui.queue.put(['updatePlants',[[random() for x in range(20)] for x in range(20)], 1.0])
			gui.queue.put(['updateAnimals',[True], [0], [(random()*50-random()*50, random()*50-random()*50)], [random()*360]])
			gui.queue.put('Output at timestep: ' + str(i+1) + '/' + str(timesteps))
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