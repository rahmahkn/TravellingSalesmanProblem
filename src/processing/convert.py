import tsp_solver

# Convert external file to Branch and Bound elements
def txtToList(txtFile):
    courierIdentity = [] # Will be filled with courier's name, pace, and delivery time
    places = [] # List of coordinates that will be visited
    file = open(txtFile, "r")

    for i in range (len(file)):
        if file[i] == "COURIER":
            courierIdentity += [file[i+1]]
            courierIdentity += [file[i+2]]
            courierIdentity += [file[i+3]]
        elif file[i] == "ORIGIN":
            coor = Coordinate(float(file[i+2], float(file[i+3], file[i+1])))
            places += [coor]
        elif file[i] == "DESTINATION":
            j = i+1
            while (j < len(file)-1):
                coor = Coordinate(float(file[j+1], float(file[j+2], file[j])))
                places += coor
                j += 3
            break;

    print(courierIdentity)
    print(places)

txtToList(r"case1.txt")

# Convert list to 

# Convert added origins to html style

# Convert list to html table

