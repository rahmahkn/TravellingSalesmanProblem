from flask import *
from processing.tsp_solver import *
from processing.util import *
from processing.database import *

app = Flask(__name__)
app.secret_key = "seleksiirk5"

class FormData():
    courierName = None
    courierPace = None
    deliveryTime = None
    coordinates = []

data = FormData()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/route/identity', methods=['POST', 'GET'])
def add_identity():
    if request.method == 'POST':
        # Getting courier identity
        data.courierName = request.form.get('courierName')
        data.courierPace = request.form.get('courierPace')
        data.deliveryTime = request.form.get('deliveryTime')

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
    P = Path(data.coordinates, G.recursiveBnB(0,0,[],G.distMatrix,0))
    routeString = P.pathToString()
    distance = P.countDistance()
    duration = distance / float(data.courierPace) # in hour
    completeTime = calculateEndTime(data.deliveryTime, duration)

    # Saving to database
    insertRecord(data.courierName, data.deliveryTime, routeString, duration, completeTime, distance)
    
    # Resetting coordinates to empty list
    data.coordinates = []
    return render_template('result.html') #, string=routeString, graph=routeGraph, cost=cost, time=completeTime

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)