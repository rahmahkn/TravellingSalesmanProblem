from flask import *
from processing.tsp_solver import *
from processing.util import *
from processing.database import *

app = Flask(__name__)
app.secret_key = "seleksiirk5"
global coordinates
coordinates = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/route', methods=['POST', 'GET'])
def add_route():
    courier = []
    global coordinates

    if request.method == 'POST':
        # Getting file
        # file = request.files['fileExt']
        # file.save(file.filename)

        # Getting courier identity
        courierName = request.form.get('courierName')
        courierPace = request.form.get('courierPace')
        deliveryTime = request.form.get('deliveryTime')
        # print(deliveryTime)
        session['courierName'] = courierName
        session['courierPace'] = courierPace

        # Getting destination information
        originName = request.form.get('startName')
        originCoorX = request.form.get('startCoorX')
        originCoorY = request.form.get('startCoorY')
        destName = request.form.get('destName')
        destCoorX = request.form.get('destCoorX')
        destCoorY = request.form.get('destCoorY')

        # Processing inputted form
        if (typeFloatSafety(originCoorX) and typeFloatSafety(originCoorY) and typeFloatSafety(originName)):
            originCoor = Coordinate(float(originCoorX), float(originCoorY), originName)
            coordinates += [originCoor]

        if (typeFloatSafety(destCoorX) and typeFloatSafety(destCoorY) and typeFloatSafety(destName)):
            destCoor = Coordinate(float(destCoorX), float(destCoorY), destName)
            coordinates += [destCoor]

        if coordinates != []:
            G = Graph(coordinates)
            routeList = G.recursiveBnB(0, 0, [], G.distMatrix, 0)
            route = Path(coordinates, routeList)
            # print(route.pathToString())

            # Get shortest route
            session['routeGraph'] = 'ceritanya graph'
            session['routeString'] = route.pathToString()
            session['deliveryTime'] = deliveryTime
            session['completeTime'] = calculateEndTime(deliveryTime, route.countDistance()/courierPace)
            session['cost'] = route.countDistance()
            
        return render_template('route.html', addedDests='ceritanya yg udah diadd')

    elif request.method == 'GET':
        return render_template('route.html')

@app.route('/route/result', methods=['POST'])
def get_route():
    global coordinates

    courierName = session.get('courierName')
    courierPace = session.get('courierPace')
    routeGraph = session.get('routeGraph')
    routeString = session.get('routeString')
    deliveryTime = session.get('deliveryTime').strftime("%Y-%m-%d, %H:%M:%S")
    completeTime = session.get('completeTime').strftime("%Y-%m-%d, %H:%M:%S")
    cost = session.get('cost')
    duration = cost/courierPace

    # Saving to database
    insertRecord(courierName, deliveryTime, routeString, duration, completeTime, cost)
    
    coordinates = []
    return render_template('result.html', string=routeString, graph=routeGraph, cost=cost, time=completeTime)

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)