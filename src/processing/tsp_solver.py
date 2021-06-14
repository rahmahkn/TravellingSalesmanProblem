import copy
import numpy as np

class Coordinate():
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
    
    # Function to count Euclidean Distance between 2 coordinates
    def eucDistance(self, otherCoor):
        return ((otherCoor.x-self.x)**2 + (otherCoor.y-self.y)**2)** 0.5

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
                result += ("→")

        return result

class Graph():
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.nbVertex = len(coordinates)
        self.distMatrix = [[coor1.eucDistance(coor2) for coor1 in (coordinates)]
                                                        for coor2 in (coordinates)]
        for i in range(self.nbVertex):
            for j in range(self.nbVertex):
                if (i == j):
                    self.distMatrix[i][j] = float('inf')

    def reduceMatrix(self, matrix, row, col, start):
        sumReduce = 0
        reducedMatrix = copy.deepcopy(matrix)

        # Making elements in "row" and "column" infinite
        # and element with index (col,row) infinite
        if (row != -1 or col != -1):
            for j in range (len(reducedMatrix[0])):
                reducedMatrix[row][j] = float('inf')

            for i in range (len(reducedMatrix[0])):
                reducedMatrix[i][col] = float('inf')

            reducedMatrix[col][row] = float('inf')

        # Preventing back to start point before end
        reducedMatrix[col][start] = float('inf')

        # Scanning rows, reducing row with its minimum element
        for i in range (len(reducedMatrix[0])):
            # If the minimum is not 0 or infinite, substract all elements in the row
            # with the minimum value
            minValue = min(reducedMatrix[i])
            if (minValue != 0 and minValue != float('inf')):
                for j in range (self.nbVertex):
                    reducedMatrix[i][j] -= minValue

                sumReduce += minValue

        # Scanning columns, reducing column with its minimum element
        for j in range (len(reducedMatrix[0])): # j is the index of column
            col = [row[j] for row in reducedMatrix]

            # If the minimum is not 0 or infinite, substract all elements in the column
            # with the minimum value
            minValue = min(col)
            if (minValue != 0 and minValue != float('inf')):            
                for i in range (self.nbVertex): # i is the index of row
                        reducedMatrix[i][j] -= minValue

                sumReduce += minValue

        return [reducedMatrix, sumReduce]

    def recursiveBnB(self, start, rootNode, route, matrix, cost):
        if (len(route) == self.nbVertex):
            return route + [start]# Route contains index that represent coordinate
        else:
            # Finding bound value for root node if there's only root node
            if (route == []):
                rootValue = (self.reduceMatrix(matrix, -1, -1, start))[1]
                route += [rootNode]
                cost = copy.deepcopy(rootValue)
                print(cost)
            
            # Initializing array to contain child nodes
            childNodesMatrix = []
            childNodesCost = []
            notVisitedNodes = list(set([i for i in range(self.nbVertex)]) - set(route))

            # Making child nodes for rootNode
            for node in notVisitedNodes:
                temp = self.reduceMatrix(matrix, rootNode, node, start)
                childNodesMatrix += [temp[0]]
                childNodesCost += [cost + self.distMatrix[rootNode][node] + temp[1]]

            # Getting promising node with minimum cost
            promisingNode = notVisitedNodes[childNodesCost.index(min(childNodesCost))]
            route += [promisingNode]
            matrix = childNodesMatrix[childNodesCost.index(min(childNodesCost))]

            return self.recursiveBnB(start, promisingNode, route, matrix, min(childNodesCost))

# Driver
C1 = Coordinate(3.5,-0.2,"Google")
C2 = Coordinate(0,2.3,"Bukalapak")
C3 = Coordinate(7.9,10,"Gojek")
C4 = Coordinate(8.1,22,"Tokopedia")
C5 = Coordinate(0.1,-11,"Amazon")

distances = [C1, C2, C3, C4, C5]
G = Graph(distances)
# G.distMatrix = [[float('inf'), 10, 17, 0 ,1],
#                 [12, float('inf'), 11, 2, 0],
#                 [0, 3, float('inf'), 0, 2],
#                 [15, 3, 12, float('inf'), 0],
#                 [11, 0, 0, 12, float('inf')]]

I = G.recursiveBnB(0, 0, [], G.distMatrix, 0)
print(I)
P = Path(distances, I)
print(P.countDistance())
print(P.pathToString())