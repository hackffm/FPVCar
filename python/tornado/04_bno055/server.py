import json
import threading
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import serial
import time

from tornado import gen
from tornado.ioloop import IOLoop

from components import *

# bno055 component
bno = Bno055()
bno_data = {}
bno_changed = threading.Condition()
bno_thread = None

# config
baud = 38400
data_serial = b''
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


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", ip_first=ip_first)


class Application(tornado.web.Application):
    def __init__(self, debug):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': './root'})
        ]

        settings = {
            'debug': debug,
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ser.flushInput()
    cmd = "v\r"
    ser.write(cmd.encode())

    for info in infos:
        print(info)

    print('start bno055 read')
    bno_thread = threading.Thread(target=read_bno)
    bno_thread.daemon = True  # Don't let the BNO reading thread block exiting.
    bno_thread.start()

    ws_app = Application(debug=debug)
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(port)

    print('Start web server at port:' + str(port))
    IOLoop.current().spawn_callback(websocket_loop)
    IOLoop.instance().start()
