import numpy as np
import cablesPF as pf

class logic :
    def __init__(self, number, grid) :
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


    def getIdsRec(self, Coords:tuple) :
        #Get the Ids of the links that have the object at "Coords" as a receiver,
        #the name stands for "Get Ids as Receiver"
        Ids = []
        for Id in range(len(self.gps)) :
            if Coords == self.gps[Id][1] :
                Ids.append(Id)
        return Ids


    def getIdsEmm(self, Coords:tuple) :
        #Get the Ids of the links that have the object at "Coords" as an emmiter,
        #the name stands for "Get Ids as Emmiter"
        Ids = []
        for Id in range(len(self.gps)) :
            if Coords == self.gps[Id][0] :
                Ids.append(Id)
        return Ids


    def getLinkState(self, Id:int) :
        return self.gps[Id][2]


    def setLinkState(self, Id:int, state:bool) :
        self.gps[Id][2] = state
        return None


    def getLinkRec(self, Id:int) :
        #returns the coordinates of the receiver of the link
        return self.gps[Id][1]


    def getPaths(self, grid:np.ndarray) :
        h, w = grid.shape
        newgrid = np.zeros((h, w), dtype=str)
        for y in range(h) :
            for x in range(w) :
                if grid[y, x] in 'ITD&|!' :
                    newgrid[y, x] = 'X'
                else :
                    newgrid[y, x] = '.'
        
        paths = []

        for link in self.gps :
            linkGrid = newgrid.copy()
            s, e = link[0], link[1]

            sGate, eGate = False, False
            if grid[s[1], s[0]] in '&|!' :
                s = (s[0], s[1]-1)
                sGate = True
            if grid[e[1], e[0]] in '&|!' :
                e = (e[0], e[1]+1)
                eGate = True

            if s == e :
                path = [s]
            else :
                linkGrid[s[1], s[0]] = 'A'
                linkGrid[e[1], e[0]] = 'B'
                path =  pf.pathFind(linkGrid)
            
            if sGate :
                path.append(link[0])
            if eGate :
                path = [link[1]] + path
                
            
            paths.append(path)
        return paths
    
    def getTruePaths(self, paths, delta) :
        truePaths = []
        nodePaths = []

        for ii in range(len(paths)) :
            path, truePath = paths[ii], []
            nodePath = chain2nodes(path)
            nodePaths.append(nodePath)

            for jj in range(len(nodePath)-1) :
                s, e = nodePath[jj], nodePath[jj+1]
                if s[0] == e[0] :
                    direction = 0
                else :
                    direction = 1
                c = countOverlap(nodePaths, s, e, direction)
                offset = getOffset(c)

                if jj == 0 :
                    truePath.append((s[0]*delta + delta//2, s[1]*delta + delta//2))
                truePath[-1] = addOffset(truePath[-1], offset, direction)
                truePath.append((e[0]*delta + delta//2, e[1]*delta + delta//2))
                truePath[-1] = addOffset(truePath[-1], offset, direction)

            truePaths.append(truePath)
        return truePaths



def chain2nodes(chain) :
    nodes = [chain[0]]
    for ii in range(1, len(chain)-1) :
        C0 = chain[ii-1]
        C1 = chain[ii]
        C2 = chain[ii+1]
        if C0[0] == C1[0] == C2[0] :
            None
        elif C0[1] == C1[1] == C2[1] :
            None
        else :
            nodes.append(C1)
    return nodes + [chain[-1]]


def getOffset(count) :
    if count%2 == 0 :
        return -count
    return count + 1


def overlap(s1, e1, s2, e2, d) :
    if s2[d] == e2[d] == s1[d] :
        if s1[1-d] <= s2[1-d] <= e1[1-d] or s1[1-d] <= e2[1-d] <= e1[1-d] :
            return True
    return False


def countOverlap(paths, s1, e1, d) :
    count = 0
    for path in paths[:-1] :
        for kk in range(len(path)-1) :
            s2, e2 = path[kk], path[kk+1]
            if overlap(s1, e1, s2, e2, d) :
                count += 1
    return count


def addOffset(C, offset, d) :
    return (C[0] + (1-d)*offset, C[1] + d*offset)