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

class Edge():
    def __init__(self, row, column):
        self.row = row
        self.column = column

    # def getName(self):
    #     return self.coor.name

class Path():
    def __init__(self, pathList):
        self.path = pathList # list of Coordinates that make the path

    # Function to count distance of a path from first to last vertex 
    def countDistance(self):
        dist = 0
        for i in range (len(self.path)-1):
            dist += self.path[i].eucDistance(self.path[i]+1)
        
        return dist

class Graph():
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.nbVertex = len(coordinates)
        self.distMatrix = [[coor1.eucDistance(coor2) for coor1 in (coordinates)]
                                                        for coor2 in (coordinates)]
        for i in range(self.nbVertex):
            for j in range(self.nbVertex):
                if (i == j):
                    self.distMatrix[i][j] = np.inf

    def reduceMatrix(self, matrix, row, col, start):
        sumReduce = 0
        reducedMatrix = copy.deepcopy(matrix)

        # Making elements in "row" and "column" infinite
        # and element with index (col,row) infinite
        if (row != -1 or col != -1):
            for j in range (len(matrix[0])):
                reducedMatrix[row][j] = np.inf

            for i in range (len(matrix[0])):
                reducedMatrix[i][col] = np.inf

            reducedMatrix[col][row] = np.inf

        # Preventing back to start point before end
        reducedMatrix[col][start] = np.inf

        # Scanning rows, reducing row with its minimum element
        for i in range (len(matrix[0])):
            counter = 0
            temp = 0

            for j in range (len(matrix[0])):
                if (reducedMatrix[i][j] != np.inf):
                    reducedMatrix[i][j] -= min(reducedMatrix[i])
                    counter += 1
                    temp += min(reducedMatrix[i])

            if (counter > 0):
                sumReduce += (temp/counter)

        # Scanning columns, reducing column with its minimum element
        for j in range (len(matrix[0])): # j is the index of column
            col = [row[j] for row in reducedMatrix]
            counter = 0
            temp = 0
            
            for i in range (len(matrix[0])): # i is the index of row
                if (reducedMatrix[i][j] != np.inf):
                    reducedMatrix[i][j] -= min(col)
                    counter += 1
                    temp += min(reducedMatrix[i])
            
            if (counter > 0):
                sumReduce += (temp/counter)

        print('Setelah direduce')
        for row in reducedMatrix:
            print(row)

        print(sumReduce)

        return [reducedMatrix, sumReduce]

    def recursiveBnB(self, start, rootNode, route, matrix, cost):
        if (len(route) == self.nbVertex):
            return route, cost # Route contains index that represent coordinate
        else:
            # Finding bound value for root node if there's only root node
            if (route == []):
                rootValue = (self.reduceMatrix(matrix, -1, -1, start))[1]
                route += [rootNode]
                cost = copy.deepcopy(rootValue)
                print(cost)
            
            # Initializing array to contain child nodes
            childNodesMatrix = []
            childNodesValue = []
            notVisitedNodes = list(set([i for i in range(self.nbVertex)]) - set(route))
            print('Not visited nodes:')
            print(notVisitedNodes)

            # Making child for rootNode
            print('\nSebelum direduce:')
            for row in matrix:
                print(row)

            for node in notVisitedNodes:
                temp = self.reduceMatrix(matrix, rootNode, node, start)
                childNodesMatrix += [temp[0]]
                childNodesValue += [cost + self.distMatrix[rootNode][node] + temp[1]]

            # Getting promising node with minimin cost
            promisingNode = notVisitedNodes[childNodesValue.index(min(childNodesValue))]
            route += [promisingNode]
            # print('Min value:')
            # print(min(childNodesValue))
            matrix = childNodesMatrix[childNodesValue.index(min(childNodesValue))]

            return self.recursiveBnB(start, promisingNode, route, matrix, min(childNodesValue))

# Driver
C1 = Coordinate(3.5,-0.2,"Google")
C2 = Coordinate(0,2.3,"Bukalapak")
C3 = Coordinate(7.9,10,"Gojek")
C4 = Coordinate(8.1,22,"Tokopedia")
C5 = Coordinate(0.1,-11,"Amazon")
# print(C1.eucDistance(C2))
# print(C1.eucDistance(C3))

distances = [C1, C2, C3, C4, C5]
G = Graph(distances)
G.distMatrix = [[np.inf, 10, 17, 0 ,1],
                [12, np.inf, 11, 2, 0],
                [0, 3, np.inf, 0, 2],
                [15, 3, 12, np.inf, 0],
                [11, 0, 0, 12, np.inf]]


# print(G.reduceMatrix(0,2))
print(G.recursiveBnB(0, 0, [], G.distMatrix, 0))
# for row in G.distMatrix:
#     print(row)