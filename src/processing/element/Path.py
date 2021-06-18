class Path():
    def __init__(self, coordinateList, indexList):
        self.coordinates = coordinateList # list of Coordinates that make the path
        self.index = indexList # list of Index that correspond to coordinateList

    # Function to count distance of a path from first to last vertex 
    def countDistance(self):
        dist = 0
        for i in range (len(self.index)-1):
            dist += self.coordinates[self.index[i]].eucDistance(self.coordinates[self.index[i+1]])
        
        return dist

    # Function to get path in string
    def pathToString(self):
        result = ''
        for i in range (len(self.index)):
            result += self.coordinates[self.index[i]].name

            if (i != len(self.index)-1):
                result += ("->")

        return result