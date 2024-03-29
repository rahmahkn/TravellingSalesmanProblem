from flask import *
from processing.convert import txtToList
from processing.element.Coordinate import Coordinate
from processing.element.Path import Path
from processing.tsp_solver import Graph
from processing.util import *
from processing.database import *
import datetime
import os

GRAPH_FOLDER = os.path.join('static', 'graphs')
TXT_FOLDER = os.path.join('upload', '')

app = Flask(__name__)
app.secret_key = "seleksiirk5"
app.config['GRAPH_FOLDER'] = GRAPH_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class FormData():
    courierName = None
    courierPace = None
    deliveryTime = None
    coordinates = []
    destinations = []
    allGraphs = []

data = FormData()

@app.route('/')
def home():
    # Resetting coordinates to empty list and deletting processed files
    data.coordinates = []
    data.destinations = []
    data.allGraphs = []
    for file in os.listdir(TXT_FOLDER):
        os.remove(os.path.join(TXT_FOLDER, file))
    for file in os.listdir(GRAPH_FOLDER):
        os.remove(os.path.join(GRAPH_FOLDER, file))

    return render_template('index.html')

@app.route('/route', methods=['POST', 'GET'])
def intro_route():
    if request.method == 'POST':
        fileExt = request.files.getlist('fileExt')
        if fileExt != []:
            for file in fileExt:
                file.save('upload/' + file.filename)
                data.allGraphs += [txtToList('upload/' + file.filename)]
        return render_template('form_intro.html')
    else:
        return render_template('form_intro.html')

@app.route('/route/identity', methods=['POST', 'GET'])
def add_identity():
    if request.method == 'POST':
        # Getting courier identity
        data.courierName = request.form.get('courierName')
        data.courierPace = request.form.get('courierPace')
        tempDate = request.form.get('deliveryDate')
        tempTime = request.form.get('deliveryTime')

        if (tempDate != None) and (tempTime != None):
            tempDate = tempDate.split('-')
            tempTime = tempTime.split(':')
            data.deliveryTime = datetime.datetime(int(tempDate[0]), int(tempDate[1]), int(tempDate[2]), int(tempTime[0]), int(tempTime[1]), 0)

        # Getting origin information
        originName = request.form.get('startName')
        originCoorX = request.form.get('startCoorX')
        originCoorY = request.form.get('startCoorY')

        # Making coordinate element
        if (originName != None) and (originCoorX != None) and (originCoorY != None):
            coor = Coordinate(float(originCoorX), float(originCoorY), originName)
            data.coordinates += [coor]
            
        return redirect(url_for('add_route'))

    elif request.method == 'GET':
        return render_template('form_identity.html')

@app.route('/route/destination', methods=['POST', 'GET'])
def add_route():
    if request.method == 'POST':
        # Getting destination information
        destName = request.form.get('destName')
        destCoorX = request.form.get('destCoorX')
        destCoorY = request.form.get('destCoorY')

        # Making coordinate element
        if (destName != None) and (destCoorX != None) and (destCoorY != None):
            coorString = [destName + " (" + str(destCoorX) + ", " + str(destCoorY) + ")"]
            data.destinations += coorString
            coor = Coordinate(float(destCoorX), float(destCoorY), destName)
            data.coordinates += [coor]
            
        return render_template('form_destination.html', destinations=data.destinations)

    elif request.method == 'GET':
        return render_template('form_destination.html')

@app.route('/route/result', methods=['POST', 'GET'])
def get_route():
    # Initializing result that will be passed to html
    result = []

    # Adding inputted data to courierIdentity and graph
    if (data.courierName != None) and (data.courierPace != None) and (data.deliveryTime != None):
        data.allGraphs += [[[data.courierName, data.courierPace, data.deliveryTime], data.coordinates]]

    # Getting all shortest paths
    count = 1
    for graph in data.allGraphs:
        G = Graph(graph[1])
        shortestPathIndex = G.recursiveBnB(0,0,[],G.distMatrix,0)

        P = Path(graph[1], shortestPathIndex)
        routeString = P.pathToString()
        distance = round(P.countDistance(), 2)
        duration = distance / float(graph[0][1]) # in hour

        if type(graph[0][2]) != str:
            deliveryTime = graph[0][2].strftime("%Y/%m/%d %H:%M:%S")
        else:
            deliveryTime = graph[0][2]
        completeTime = calculateEndTime(graph[0][2], duration)
        completeTime = completeTime.strftime("%Y/%m/%d %H:%M:%S")

        # Make graph visualizations
        saveVisualizations(indexToXY(shortestPathIndex, graph[1]), graph[1], count)
        filename = [('graph' + str(count) + '-' + str(i) + '.png') for i in range (len(graph[1])+1)]
        count += 1

        # Saving to database
        insertRecord(graph[0][0], deliveryTime, routeString, duration, completeTime, distance)

        # Add to result that will be passed to html
        result += [[str(routeString.replace('->', '→')), str(distance), str(completeTime), filename]]

    return render_template('result.html', resultList=result)

@app.route('/history', methods=['POST', 'GET'])
def history():
    if request.method == 'POST':
        searchCourier = request.form.get("searchCourier")
        searchDate = request.form.get("searchDate")

        result = searchRecord(searchCourier, searchDate)

        return render_template('history.html', searchResult=result)
    else:
        return render_template('history.html')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)