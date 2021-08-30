import numpy as np

class logic :
    def __init__(self, number) :
        self.nb = str(number)
        longnb = (3-len(self.nb))*"0" + self.nb
        self.dir = "logic\links" + longnb + ".txt"
        
        try :
            File = open(self.dir)
            Text = File.read()
            File.close()
            self.makeLog = True
        except :
            self.makeLog = False
            self.gps = []
        
        if self.makeLog :
            lines = Text.split('\n')
            groups = [line.split(' ') for line in lines]
            for k in range(len(groups)) :
                x1, y1, x2, y2 = groups[k]
                groups[k] = [(int(x1), int(y1)), (int(x2), int(y2)), False]
            self.gps = groups
            #For each link (line),
            #the first couple is the coordinates of the emitter,
            #the second couple is the coordinates of the receiver
            #and the bool is the state of the link.


    def getAll(self) :
        return self.gps


    def getIdsRec(self, Coords) :
        #Get the Ids of the links that have the object at "Coords" as a receiver,
        #the name stands for "Get Ids as Receiver"
        Ids = []
        for Id in range(len(self.gps)) :
            if Coords == self.gps[Id][1] :
                Ids.append(Id)
        return Ids


    def getIdsEmm(self, Coords) :
        #Get the Ids of the links that have the object at "Coords" as an emmiter,
        #the name stands for "Get Ids as Emmiter"
        Ids = []
        for Id in range(len(self.gps)) :
            if Coords == self.gps[Id][0] :
                Ids.append(Id)
        return Ids


    def getLinkState(self, Id) :
        return self.gps[Id][2]


    def setLinkState(self, Id, state) :
        self.gps[Id][2] = state
        return None


    def getLinkRec(self, Id) :
        #returns the coordinates of the receiver of the link
        return self.gps[Id][1]
        