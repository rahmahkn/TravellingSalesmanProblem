from flask import *
from processing.tsp_solver import *
from processing.util import *

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
        print(deliveryTime)

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
            print(route.pathToString())

            # Save to database

            # Get shortest route
            session['routeString'] = route.pathToString()
            session['routeGraph'] = 'ceritanya graph'
            session['cost'] = route.countDistance()
            session['completeTime'] = deliveryTime

        return render_template('route.html', addedDests='ceritanya yg udah diadd')
    elif request.method == 'GET':
        return render_template('route.html')

@app.route('/route/result', methods=['POST'])
def get_route():
    global coordinates
    routeString = session.get('routeString')
    routeGraph = session.get('routeGraph')
    cost = session.get('cost')
    completeTime = session.get('completeTime')

    coordinates = []
    return render_template('result.html', string=routeString, graph=routeGraph, cost=cost, time=completeTime)

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)