
from math import sin, cos, pi
from InitializeAnimals import AnimalBirthWrapper


def AnimalsRun(Animals,CurrentAnimals,Alive,Or,MapSize,gui,time):
    
    GrowEff=.5
    for i in range(len(Alive)):
        if Alive[i]:
            
            
    #Or[i][0]=Orders.Accelerate
    #Or[i][1]=Orders.Turn
    #Or[i][2]=Orders.Attack
    #Or[i][3]=Orders.Reproduce
    #Or[i][4]=Orders.Grow
            Animals[i].V+=Or[i][0]
            Animals[i].T=((Animals[i].T+Or[i][1] +180.0) % 360.0 ) -180.0
            Animals[i].X[0]=(Animals[i].X[0] + Animals[i].V*cos(Animals[i].T/180.0*pi)) % MapSize
            Animals[i].X[1]=(Animals[i].X[1] + Animals[i].V*sin(Animals[i].T/180.0*pi)) % MapSize
            
            if Or[i][4]>0:
                Animals[i].Size+=Or[i][4]*GrowEff
            elif Or[i][4]<0:
                Animals[i].Size+=Or[i][4]/GrowEff
            Animals[i].Size+=-Or[i][3]
            if Or[i][3]>0:
                Alive.append(True)
                CurrentAnimals.append(CurrentAnimals[i])
                Animals.append(AnimalBirthWrapper(Or[i][3]/4, Or[i][3]/4, Or[i][3]/8, Or[i][3]/8, Animals[i]))
                
                PrintSize = [Animals[-1].Size**.5/100/MapSize]
                PrintTheta = [Animals[-1].T+180]
           	PrintColor = [Animals[-1].Color]
           	PrintOldX = [[Animals[-1].X[0]/MapSize, Animals[-1].X[1]/MapSize]]
           	gui.queue.put(['initializeAnimals',PrintColor, PrintSize, PrintOldX, PrintTheta]) 
   	        gui.queue.put('An Animal was born')
   	        Or.append([0,0,0,0,0,0])
   	        Animals[-1].Color
   	        
   	           	           	        
    for i in range(len(Alive)):
        if Alive[i]:
            if Or[i][2]>0:
                print 'TBD'
    for i in range(len(Alive)):
        if Alive[i]:
            if Animals[i].Size<=0:
                gui.queue.put('Animal has metabolized its entire body')
                gui.queue.put(['kill',i])
                Alive[i]=False
                Animals[i].Size=0
            elif Animals[i].Calories<=0:
                gui.queue.put('Animal has Starved to death')
                gui.queue.put(str([Animals[i].Calories,Animals[i].Size,Animals[i].Stomach]))
                gui.queue.put(['kill',i])
                Alive[i]=False
            elif Animals[i].Health<=0:
                gui.queue.put('Animal has been slain')
                gui.queue.put(['kill',i])
                Alive[i]=False
                
        