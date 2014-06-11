#/usr/bin/python

class MineWrapper():
    def __init__(self,CS):
        self.Size=CS
    

class MineBirthWrapper():
    def __init__(self,NW):
        self.Size=NW.Size

Mine=[]
Mine.append(MineWrapper(66))
Mine.append(MineBirthWrapper(Mine[0]))

Mine[1].Size=44
print Mine[0].Size

Mine[0].Size=88
print Mine[1].Size


print 500 %400