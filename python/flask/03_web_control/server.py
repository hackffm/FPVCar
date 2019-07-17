#!/usr/bin/env python3
import json

from flask import Flask, render_template
from flask import request, jsonify
from flask_socketio import SocketIO, emit

from components import Base

app = Flask(__name__)
socketio = SocketIO(app)

debug = True
components = {
    "base": Base()
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/fpvc/api/base", methods=['POST'])
def move_base_to_postion():
    move = request.get_json(force=True)
    return jsonify(move)


@app.route("/fpvc/api/doShutdown")
def shutdown():
    return "shutting down!"


@app.route("/fpvc/api/eye/left", methods=['POST'])
def move_eye():
    move = request.get_json(force=True)
    return jsonify(move)


@app.route("/fpvc/api/message", methods=['POST'])
def message_send():
    # message muss {'message': 'value'} sein
    message = request.form['message']
    result = 'Send to server:' + message
    return result


@app.route("/fpvc/api/move", methods=['POST'])
def move_base_command():
    result = 'I can not do that !'
    try:
        requested = request.get_json(force=True)
        if not 'component' in requested:
            return result
        if requested['component'] in components:
            message = requested['message']
            component = components[requested['component']]
            result = component.handleMessage(message)
        if debug:
            print('[move_base_command]result:' + str(result))
    except Exception as e:
        return e
    return result


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    emit('my response', 'response')


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')
