from flask import Flask, request, jsonify
from orientationAdjuster import OrientationAdjuster
from uwbConnectivity import UwbConnectivity
from sensorFusion import SensorFusion

app = Flask(__name__)

orientationAdjuster = OrientationAdjuster()
uwbConnectivity = UwbConnectivity()

@app.route('/', methods=['POST'])
def iotServer():
    print(request.json)

    angle = orientationAdjuster.getAngle(request.json)
    print(angle)

    position = {}
    while not position:
        print("Getting position from uwb device")
        position = uwbConnectivity.getPositionFromTag()

    x = position['position_data']['x']
    y = position['position_data']['y']
    print(x)
    print(y)

    devicesList = SensorFusion(angle, x, y).retrieveViableDevices()
    print(devicesList)

    return jsonify({"status":"success", "id":devicesList})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, use_debugger=False)
