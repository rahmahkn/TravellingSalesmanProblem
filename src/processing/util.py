import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Function to calculate end time from start time with a duration
def calculateEndTime(startTime, durationHour):
    return startTime + datetime.timedelta(seconds=3600*durationHour)

# Function to convert listOfIndex to listOfCoordinate
def indexToXY(indexList, coordinateList):
    result = []
    for idx in indexList:
        result += [[coordinateList[idx].x, coordinateList[idx].y]]
    return result

# Function to save images that visualize the route
def saveVisualizations(listOfXY, coordinateList, numbGraph):
    # Make x list and y list
    xList = [listOfXY[i][0] for i in range (len(listOfXY))]
    yList = [listOfXY[i][1] for i in range (len(listOfXY))]

    for i in range (len(listOfXY)):
        # Make points
        plt.scatter(xList, yList)
        for coor in coordinateList:
            plt.annotate(coor.name, (coor.x, coor.y))

        # Make lines
        for j in range (i):
            plt.plot([listOfXY[j][0], listOfXY[j+1][0]], [listOfXY[j][1], listOfXY[j+1][1]], marker='o')

        plt.savefig('static/graphs/graph' + str(numbGraph) + '-' + str(i) + '.png')
        plt.cla()
        plt.close()