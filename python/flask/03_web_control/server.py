#!/usr/bin/env python3
from flask import Flask, render_template
from flask import request, jsonify
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/robota/api/doShutdown")
def shutdown():
    return "shutting down!"


@app.route("/robota/api/move", methods=['POST'])
def move_base_command():
    move = request.form['move']
    result = 'moving base:' + str(move)
    return result


@app.route("/robota/api/base", methods=['POST'])
def move_base_to_postion():
    move = request.get_json(force=True)
    return jsonify(move)


@app.route("/robota/api/eye/left", methods=['POST'])
def move_eye():
    move = request.get_json(force=True)
    return jsonify(move)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    emit('my response', 'response')


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')
