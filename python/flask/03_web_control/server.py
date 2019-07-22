#!/usr/bin/env python3
from flask import Flask, render_template
from flask import request, jsonify
from flask_socketio import SocketIO, emit

from components import Base
from handlers import handler_default

app = Flask(__name__)
socketio = SocketIO(app)

debug = True
components = {
    "base": Base(handler_default)
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/fpvc/api/base", methods=['POST'])
def move_base_to_postion():
    # required by CanvasJoystik
    move = request.get_json(force=True)
    return jsonify(move)


@app.route("/fpvc/api/doShutdown")
def shutdown():
    return "shutting down!"


@app.route("/fpvc/api/message", methods=['POST'])
def message_send():
    # message muss {'message': 'value'} sein
    message = request.form['message']
    result = 'Send to server:' + message
    return result


@app.route("/fpvc/api/component", methods=['POST'])
def message_component():
    result = 'I can not do that !'
    try:
        requested = request.get_json(force=True)
        if debug:
            print('message_component received:' + str(requested))
        if 'component' not in requested:
            return result
        if requested['component'] in components:
            component = components[requested['component']]
            result = component.handle_message(requested)
        if debug:
            print('[message_component]result:' + str(result))
    except Exception as e:
        return e
    return result


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('my event')
def handle_my_custom_event(_json):
    print('received json: ' + str(_json))
    emit('my response', 'response')


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')
