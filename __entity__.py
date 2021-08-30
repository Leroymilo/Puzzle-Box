

class entity :
    def __init__(self, coordinates, type) :
        self.x, self.y = coordinates
        self.Type = type
        self.dir = None


    def getCoords(self) :
        return (self.x, self.y)


    def setCoords(self, coords) :
        self.x, self.y = coords
        return None


    def getDir(self) :
        return self.dir


    def setDir(self, direction) :
        self.dir = direction
        return None


    def getType(self) :
        return self.Type


    def copy(self) :
        entCopy = entity(self.getCoords(), self.getType)
        entCopy.setDir(self.getDir())
        return entCopy
