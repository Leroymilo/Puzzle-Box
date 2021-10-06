"""
This is the algorithm used to determine
the path of the cables through the grid.
It's basically a pathfinder without diagonals,
prioritizing paths with fewer turns.
"""

import numpy as np

class square :
    def __init__ (self, coords, parent=None, B=None) :
        self.C = coords
        self.p = parent
        if B is None :
            self.F = np.inf
        else :
            self.F = getGcost(self) + getHcost(self, B)
    

    def isTurn(self) :
        pSq = self.p
        if pSq is not None :
            ppSq = pSq.p
            if ppSq is not None :
                if self.C[0] == pSq.C[0] == ppSq.C[0] :
                    None
                elif self.C[1] == pSq.C[1] == ppSq.C[1] :
                    None
                else :
                    return True
        return False


    def getPath(self) :
        Path = [self]
        G = 0
        while Path[-1].p is not None :
            Path.append(Path[-1].p)
        return Path


def getHcost(sq1:square, sq2:square) :
    H = 0
    x, y = sq1.C
    xT, yT = sq2.C
    while (x, y) != (xT, yT) :
        if x != xT :
            H += 10
            if x > xT :
                x -= 1
            else :
                x += 1
        if y != yT :
            H += 10
            if y > yT :
                y -= 1
            else :
                y += 1
    return H


def getGcost(sq:square) :
    G = 0
    path = sq.getPath()
    for sqi in path[:-1] :
        if sqi.isTurn() :
            G += 4
        G += getHcost(sqi, sqi.p)
    return G


def minF(open) :
    minf = np.inf
    minSq = None
    for sq in open :
        if sq.F <= minf :
            minf = sq.F
            minSq = sq
    return minSq


def add2open(sq:square, grid:np.ndarray, open, closed, B:square) :
    w, h = grid.shape
    x, y = sq.C
    nC = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
    traversable = True

    for i in range(len(nC)) :
        nbx, nby = nC[i]
        if nbx < 0 or nbx >= w or nby < 0 or nby >= h :
            traversable = False
        if traversable and grid[nby, nbx] == 'X' :
            traversable = False
        for cSq in closed :
            if cSq.C == (nbx, nby) :
                traversable = False
        for oSq in open :
            if oSq.C == (nbx, nby) :
                if oSq.F < sq.F :
                    traversable = False
                elif oSq.F > sq.F :
                    open.remove(oSq)

        if traversable :
            open.append(square((nbx, nby), sq, B))
        traversable = True
    return None


def pathFind(grid:np.ndarray) :
    h, w = grid.shape

    for y in range(h) :
        for x in range(w) :
            if grid[y, x] == 'A' :
                A = square((x, y))
            elif grid[y, x] == 'B' :
                B = square((x, y))
    
    closed = [A]
    open = []
    add2open(A, grid, open, closed, B)
    search = True

    while len(open) != 0 :
        curSq = minF(open)

        #drawgrid(grid, open, closed)
        
        if curSq.C == B.C :
            path = curSq.getPath()
            return [sq.C for sq in path]
            #We don't need to return whole square objects,
            #only their coordinates are needed.
        
        open.remove(curSq)
        closed.append(curSq)
        add2open(curSq, grid, open, closed, B)
    
    print("error : too much logic, can't place cables")
    return None


def drawgrid(grid, open, closed) :
    #Debugging the pathfinding
    gridC = grid.copy()
    for sq in open :
        x, y = sq.C
        gridC[y, x] = 'o'
    print(gridC)
    for sq in closed :
        x, y = sq.C
        gridC[y, x] = 'c'
    print(gridC)