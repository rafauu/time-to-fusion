from flask import Flask, request, jsonify
from uwbConnectivity import UwbConnectivity
from orientationAdjuster import OrientationAdjuster
from sensorFusion import SensorFusion
import bluepy.btle
from database import Database

app = Flask(__name__)

peripheral = bluepy.btle.Peripheral(Database().getMacAddress())

@app.route('/', methods=['POST'])
def iotServer():
    global peripheral
    print(request.json)

    angle = OrientationAdjuster(request.json).getAngle()
    print(angle)

    position = {}
    while not position:
        print("Getting position from uwb device")
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
