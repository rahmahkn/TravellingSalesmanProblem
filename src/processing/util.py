import datetime
import matplotlib.pyplot as plt

# Function to check if a variable can be converted to float
def typeFloatSafety(element):
    return ((type(element) is str) or (type(element) is int)) and (element != '')

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
def saveVisualizations(listOfXY, numbGraph):
    for i in range (len(listOfXY)-1):
         plt.plot([listOfXY[i][0], listOfXY[i+1][0]], [listOfXY[i][1], listOfXY[i+1][1]], marker='o')
    plt.savefig('static/graphs/graph' + str(numbGraph) + '.png')
    plt.cla()

# Function to get image with active coordinates
# def getActiveCoordiantes(listOfActiveCoordinate):

# saveVisualizations([[1,2],[7,5],[3,4],[1,2]])