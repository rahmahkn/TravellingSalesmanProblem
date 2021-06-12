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
    def __init__(self):
        self.path = [] # list of Coordinates that make the path

    # Function to count distance of a path from first to last vertex 
    def countDistance(self):
        dist = 0
        for i in range (len(self.path)-1):
            dist += self.path[i].eucDistance(self.path[i]+1)
        
        return dist

    # Procedure to add vertex to last element in path
    def addToPath(self, vertex):
        self.path += vertex

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

    def reduceMatrix(self):
        sumReduce = 0

        # Scanning rows, reducing row with its minimum element
        for i in range (self.nbVertex):
            for j in range (self.nbVertex):
                self.distMatrix[i][j] -= min(self.distMatrix[i])
                sumReduce += min(self.distMatrix[i])

        # print()
        # for row in self.distMatrix:
        #     print(row)

        # Scanning columns, reducing column with its minimum element
        for j in range (self.nbVertex): # j is the index of column
            col = [row[j] for row in self.distMatrix]
            
            for i in range (self.nbVertex): # i is the index of row
                self.distMatrix[i][j] -= min(col)
                sumReduce += min(col)

        print()
        for row in self.distMatrix:
            print(row)

    def getRoute(self):
        tempMatrix = self.distMatrix
        route = []

        # Scanning rows that have only one '0' and blocking column j
        # with j is index where '0' is found in scanned row
        for i in range (self.nbVertex):
            if tempMatrix[i].count(0) == 1:
                j = tempMatrix[i].index(0)

                # Checking if edge is already in the route
                if (route.count(Edge(i,j)) == 0):
                    route += [Edge(i,j)]

                # Blocking the elements with column j in every row
                for idx in range (self.nbVertex):
                    tempMatrix[idx][j] = float('inf')

        # Scanning columns that have only one '0' and blocking every row with column index jdx
        # with jdx is index where '0' is found in scanned column
        for j in range (self.nbVertex): # j is the index of column
            col = [row[j] for row in self.distMatrix]
            
            # Checking if edge is already in the route
            if col.count(0) == 1:
                jdx = col.index(0)
                if (tempMatrix[i].count(Edge(i,jdx)) == 0):
                    route += [Edge(i,jdx)]

                for i in range (self.nbVertex): # i is the index of row
                    tempMatrix[i][jdx] = float('inf')

        # print(len(route))
        # Scanning columns again
        for j in range (self.nbVertex): # j is the index of column
            col = [row[j] for row in self.distMatrix]
            
            # Checking if edge is already in the route
            if col.count(0) == 1:
                jdx = col.index(0)
                if (tempMatrix[i].count(Edge(i,jdx)) == 0):
                    route += [Edge(i,jdx)]

                for i in range (self.nbVertex): # i is the index of row
                    tempMatrix[i][jdx] = float('inf')

        print()
        for row in tempMatrix:
            print(row)

        # Get ordered routes
        for v in route:
            print("Row: "+str(v.row)+". Col: "+str(v.column))
        orderedRoute = [route[0]]

        for i in range (self.nbVertex):
            if route[i].row == orderedRoute[0].column:
                orderedRoute += [route[i]]

        # for v in orderedRoute:
        #     print("Row: "+str(v.row)+". Col: "+str(v.column))

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

for row in G.distMatrix:
    print(row)

G.reduceMatrix()
G.getRoute()
# for row in G.distMatrix:
#     print(row)