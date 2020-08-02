from flask import Flask, request, jsonify
from uwbConnectivity import UwbConnectivity
from orientationAdjuster import OrientationAdjuster

app = Flask(__name__)

@app.route('/', methods=['POST'])
def iotServer():
    print(request.json)

    angle = OrientationAdjuster(request.json).getAngle()

    #position = UwbConnectivity().getPositionFromTag()['position_data']
    #x = position['x']
    #y = position['y']

    print(angle)
    #print(x)
    #print(y)

    return jsonify({"id":7})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, use_debugger=False)
