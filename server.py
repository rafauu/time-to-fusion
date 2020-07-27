from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def iotServer():
    return "aaa"

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port='80', threaded=True)
    app.run(host='0.0.0.0', port=80, threaded=True, use_debugger=False)
