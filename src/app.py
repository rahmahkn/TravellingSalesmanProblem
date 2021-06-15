from flask import *
from processing.tsp_solver import *

app = Flask(__name__)
app.secret_key = "seleksiirk5"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/route', methods=['POST', 'GET'])
def add_route():
    courier = []
    places = []
    if request.method == 'POST':
    # Getting data from form
        # file = request.files["fileExt"]
        # file.save(file.filename)
        # Getting courier identity
        courierName = request.form.get('courierName')
        courierPace = request.form.get('courierPace')
        deliveryTime = request.form.get('deliveryTime')

        # Getting destination information
        originName = request.form.get('startName')
        originCoorX = request.form.get('startCoorX')
        originCoorY = request.form.get('startCoorY')
        destName = request.form.get('destName')
        destCoorX = request.form.get('destCoorX')
        destCoorY = request.form.get('destCoorY')

        # Processing inputted form
        # Save to database

        # Get shortest route
        session['routeString'] = 'ceritanya string'
        session['routeGraph'] = 'ceritanya graph'
        session['cost'] = 'ceritanya cost'
        session['completeTime'] = 'ceritanya waktu'

        # destCoors += [Coordinate(float(destCoorX), float(destCoorY), destName)]
        return render_template('route.html', addedOrigin=destName)
    else:
        return render_template('route.html')

@app.route('/route/result', methods=['POST'])
def get_route():
    routeString = session.get('routeString')
    routeGraph = session.get('routeGraph')
    cost = session.get('cost')
    completeTime = session.get('completeTime')

    return render_template('result.html', string=routeString, graph=routeGraph, cost=cost, time=completeTime)

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)