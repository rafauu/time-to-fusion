from flask import Flask, request, jsonify
from uwbConnectivity import UwbConnectivity
from orientationAdjuster import OrientationAdjuster
from sensorFusion import SensorFusion

app = Flask(__name__)

@app.route('/', methods=['POST'])
def iotServer():
    print(request.json)

    angle = OrientationAdjuster(request.json).getAngle()

    position = UwbConnectivity().getPositionFromTag()
    if not position:
        return jsonify({"status":"uwbConnectionFailure"})

    x = position['position_data']['x']
    y = position['position_data']['y']

    #x = 117
    #y = 127
    print(angle)
    print(x)
    print(y)
    devicesList = SensorFusion(angle, x, y).retrieveViableDevices()
    print(devicesList)

    return jsonify({"status":"success", "id":devicesList})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, use_debugger=False)
