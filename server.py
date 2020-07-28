from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def iotServer():
    print(request.json)
    return jsonify({"id":7})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, use_debugger=False)
