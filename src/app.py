from flask import *
from processing.tsp_solver import *
from processing.util import *
from processing.database import *
import datetime
import os

GRAPH_FOLDER = os.path.join('static', 'graphs')

app = Flask(__name__)
app.secret_key = "seleksiirk5"
app.config['UPLOAD_FOLDER'] = GRAPH_FOLDER

class FormData():
    courierName = None
    courierPace = None
    deliveryTime = None
    coordinates = []

data = FormData()

@app.route('/')
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'graph1.png')
    return render_template('index.html', graph=full_filename)

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
            print(coor.name)
            data.coordinates += [coor]
            
        return render_template('form_identity.html')

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
            coor = Coordinate(float(destCoorX), float(destCoorY), destName)
            print(coor.name)
            data.coordinates += [coor]
            
        return render_template('form_destination.html')

    elif request.method == 'GET':
        return render_template('form_destination.html')

@app.route('/route/result', methods=['POST'])
def get_route():
    # Getting shortest path
    G = Graph(data.coordinates)
    shortestPathIndex = G.recursiveBnB(0,0,[],G.distMatrix,0)

    P = Path(data.coordinates, shortestPathIndex)
    routeString = P.pathToString()
    distance = P.countDistance()
    duration = distance / float(data.courierPace) # in hour

    completeTime = calculateEndTime(data.deliveryTime, duration)
    deliveryTime = data.deliveryTime.strftime("%Y/%m/%d %H:%M:%S")
    completeTime = completeTime.strftime("%Y/%m/%d %H:%M:%S")

    # Make graph
    print(indexToXY(shortestPathIndex, data.coordinates))
    saveVisualizations(indexToXY(shortestPathIndex, data.coordinates))
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'graph1.png')

    # Saving to database
    insertRecord(data.courierName, deliveryTime, routeString, duration, completeTime, distance)
    
    # Resetting coordinates to empty list
    data.coordinates = []
    return render_template('result.html', string=routeString, graph=full_filename, distance=distance, time=completeTime)

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)