from flask import *
from processing.tsp_solver import *

app = Flask(__name__)
global destNames, destCoors
destNames, destCoors = [], []

@app.route('/', methods=['POST', 'GET'])
def index():
    global destNames, destCoors

    # Getting data from form
    courierName = request.form.get("courierName")
    courierPace = request.form.get("courierPace")
    originName = request.form.get("startName")
    originCoorX = request.form.get("startCoorX")
    originCoorY = request.form.get("startCoorY")
    destName = request.form.get("destName")
    destCoorX = request.form.get("destCoorX")
    destCoorY = request.form.get("destCoorY")

    if (destNames != [] or destCoors != []):
        destNames += [destName]
        destCoors += [Coordinate(float(destCoorX), float(destCoorY), destName)]

    print(destNames)
    print(destCoors)

    return render_template('index.html', addedOrigin=destName)

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)