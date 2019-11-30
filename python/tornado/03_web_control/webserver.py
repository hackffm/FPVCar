import asyncio
import json
import os
import tornado.web
import tornado.websocket
import tornado.httpserver
import serial

from tornado import gen
from tornado.ioloop import IOLoop

from components import *
from resources import *
from web_handlers import *


# bno055 component
bno = Bno055()
bno_data = {}
bno_changed = threading.Condition()
bno_thread = None


# config
baud = 38400
debug = True
port = 9090


# run info
helper = Helper()
infos = helper.infos_self()
infos.append(port)
ip_first = helper.interfaces_first()

ser = serial.Serial('/dev/ttyS0', baud)


# load components statically
components = {
    "base": Base(ser, debug=debug),
    "stats": Stats(ser, debug=debug)
}


def read_bno():
    while True:
        with bno_changed:
            bno_data['euler'] = bno.euler()
            bno_data['temp'] = bno.temperature()
            bno_data['quaternion'] = bno.quaternion()
            bno_data['calibration'] = bno.calibration_status()
            bno_changed.notifyAll()
        time.sleep(0.1)


async def read_sensor():
    with bno_changed:
        bno_changed.wait()
        heading, roll, pitch = bno_data['euler']
        temp = bno_data['temp']
        x, y, z, w = bno_data['quaternion']
        sys, gyro, accel, mag = bno_data['calibration']
    data = {'heading': heading, 'roll': roll, 'pitch': pitch, 'temp': temp,
            'quatX': x, 'quatY': y, 'quatZ': z, 'quatW': w,
            'calSys': sys, 'calGyro': gyro, 'calAccel': accel, 'calMag': mag }

    # data_sensor = sensor.handleMessage({'sensor': 'all'})
    return data


async def serial_read():
    data = b''

    wait_bytes = ser.inWaiting();

    if not wait_bytes:
        ser.write("v\r".encode())

    for i in range(ser.inWaiting()):
        b = ser.read(1)
        if b != b'\r':
            if b == b'\n':
                return data
            else:
                data += b
    return False


async def websocket_loop():
    while True:
        data_sensor = await read_sensor()
        websocket_write({"sensor": data_sensor})

        data_serial = await serial_read()
        if data_serial:
            websocket_write(data_serial.decode("utf-8"))

        await gen.sleep(0.3)


def websocket_write(message):
    if type(message) == dict:
        message = json.dumps(message)
        [con.write_message(message) for con in WebSocketHandler.connections]
    else:
        [con.write_message(message) for con in WebSocketHandler.connections]


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)
        print('new connection was opened')
        pass

    def on_close(self):
        self.connections.remove(self)
        print('connection closed')
        pass

    def on_message(self, message):
        if debug:
            print('from WebSocket: ', message)
        m = json.loads(message)
        if 'component' in m:
            if m['component'] in components:
                component = components[m["component"]]
                result = component.handleMessage(m)
                if result:
                    result = {str(m["component"]): result}
                    websocket_write(result)
                    if debug:
                        print(result)



class WebApplication(tornado.web.Application):
    def __init__(self, components, debug):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'

        handlers = [
            (r'/', HandlerIndexPage, dict(helper=helper)),
            (r'/fpvcar/api/base', HandlerBase),
            (r'/fpvcar/api/component', HandlerComponent, dict(components=components, debug=debug)),
            (r'/fpvcar/(.*)', tornado.web.StaticFileHandler, {'path': web_resources}),
            (r'/shutdown', HandlerShutdown),
            (r'/websocket', WebSocketHandler)
        ]

        settings = {
            'autoreload': debug,
            'debug': debug,
            'static_path': web_resources,
            'template_path': 'web_templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class WebServer:
    def __init__(self, debug):
        self.name = 'webserver'

        ser.flushInput()
        cmd = "v\r"
        ser.write(cmd.encode())

        for info in infos:
            print(info)

        print('start bno055 read')
        bno_thread = threading.Thread(target=read_bno)
        bno_thread.daemon = True  # Don't let the BNO reading thread block exiting.
        bno_thread.start()

        ws_app = WebApplication(components, debug)
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(port)

        print('Start web server at port:' + str(port))
        IOLoop.current().spawn_callback(websocket_loop)
        IOLoop.instance().start()
