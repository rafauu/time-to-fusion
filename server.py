from flask import Flask, request, jsonify
from uwbConnectivity import UwbConnectivity
from orientationAdjuster import OrientationAdjuster
from sensorFusion import SensorFusion
import bluepy.btle

app = Flask(__name__)

peripheral = bluepy.btle.Peripheral("11:22:33:44:55:66")

@app.route('/', methods=['POST'])
def iotServer():
    global peripheral
    print(request.json)

    angle = OrientationAdjuster(request.json).getAngle()
    print(angle)

    position = {}
    while not position:
        print("Uwb device did not return position, retrying")
        position = UwbConnectivity(peripheral).getPositionFromTag()

    x = position['position_data']['x']
    y = position['position_data']['y']
    print(x)
    print(y)

    devicesList = SensorFusion(angle, x, y).retrieveViableDevices()
    print(devicesList)

    return jsonify({"status":"success", "id":devicesList})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, use_debugger=False)
