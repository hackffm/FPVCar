from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import serial
import threading
import time
import socket
import json
from base_rl import *

data = b''
app = Flask(__name__)
socketio = SocketIO(app)
ser = serial.Serial('/dev/ttyS0', 38400)
#base = Base(ser)
hostname = socket.gethostname()
print(hostname)

components = {
    "base": Base(ser),
    "sound": Sound(ser)
}


def handle_data(data):
    print(data)

def read_from_port(ser):
    global data
    while True:
        for i in range(ser.inWaiting()):
                b = ser.read(1)
                if(b != b'\r'): 
                    if(b == b'\n'):
                        print('msg from arduino: ', data)
                        socketio.emit('my response', data.decode("utf-8"))
                        data = b''
                    else:
                        data += b
                       
        time.sleep(0.1)

thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

@app.route("/")
def home():
	return render_template("index.html", hostname=hostname)

@app.route("/helloworld")
def helloworld():
	return "Hello, World!"

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    m = json.loads(message)
    #print(m["right"])
    component = components[m["module"]]
    component.handleMessage(m)

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received json: ' + str(json))
	emit('my response', 'echo: '+str(json))

if __name__ == "__main__":
	socketio.run(app, debug=True, port=8080, host='0.0.0.0')
	

