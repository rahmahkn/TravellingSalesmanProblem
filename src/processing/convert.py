import os, sys
from tsp_solver import Coordinate

# Convert external file to Branch and Bound elements
def txtToList(txtFile):
    courierIdentity = [] # Will be filled with courier's name, pace, and delivery time
    places = [] # List of coordinates that will be visited
    file = open(os.path.join(sys.path[0], "case1.txt"), 'r')
    lines = file.readlines()

    for i in range (len(lines)):
        if lines[i] == "COURIER\n":
            courierIdentity += [lines[i+1].rstrip("\n")] # Courier name
            courierIdentity += [float(lines[i+2].rstrip("\n"))] # Courier pace
            courierIdentity += [lines[i+3].rstrip("\n")] # Delivery time
        elif lines[i] == "ORIGIN\n":
            coor = [Coordinate(float(lines[i+2].rstrip("\n")), float(lines[i+3].rstrip("\n")), lines[i+1].rstrip("\n"))]
            places += [coor]
        elif lines[i] == "DESTINATION\n":
            j = i+1
            while (j < len(lines)-1):
                coor = [Coordinate(float(lines[j+1].rstrip("\n")), float(lines[j+2].rstrip("\n")), lines[j].rstrip("\n"))]
                places += coor
                j += 3
            break;

    print(courierIdentity)
    print(places)

txtToList('case1.txt')

# Convert list to 

# Convert added origins to html style

# Convert list to html table

