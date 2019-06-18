from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/helloworld")
def helloworld():
	return "Hello, World!"

@socketio.on('message')
def handle_message(message):
	print('received message: ' + message)

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received json: ' + str(json))
	emit('my response', 'response')

if __name__ == "__main__":
	socketio.run(app, debug=True, port=8080, host='0.0.0.0')
