import json
import os
import serial
import sys
import threading
import tornado.web
import tornado.websocket
import tornado.httpserver
import time

from multiprocessing import Process
from time import sleep
from tornado import gen
from tornado.ioloop import IOLoop

from components import *
from resources import *
from web_handlers import *


# bno055 component preparation
sensor_bno_data = {}
bno_changed = threading.Condition()


# resources
config = Config()
helper = Helper()
p1 = 'webserver process'

cfg = config.cfg()
ser = serial.Serial('/dev/ttyS0', cfg.baud)


# load components statically
components = {
    "base": Base(ser, debug=cfg.debug),
    "cam": Cam(ser, debug=cfg.debug),
    "config": ComponentConfig(config, debug=cfg.debug),
    "sound": Sound(ser, debug=cfg.debug),
    "stats": Stats(ser, debug=cfg.debug)
}


if cfg.sensors.bno055:
    from components.bno055 import Bno055
    components["sensor_bno"] = Bno055(debug=cfg.debug)


def read_bno():
    while True:
        with bno_changed:
            component = components["sensor_bno"]
            sensor_bno_data = component.handleMessage({'bno055': 'all'})
            #sensor_bno_data['euler'] = sensor_bno.euler()
            #sensor_bno_data['temp'] = sensor_bno.temperature()
            #sensor_bno_data['quaternion'] = sensor_bno.quaternion()
            #sensor_bno_data['calibration'] = sensor_bno.calibration_status()
            bno_changed.notifyAll()
        time.sleep(0.1)


async def read_sensor():
    with bno_changed:
        bno_changed.wait()
        heading, roll, pitch = sensor_bno_data['euler']
        temp = sensor_bno_data['temp']
        x, y, z, w = sensor_bno_data['quaternion']
        sys, gyro, accel, mag = sensor_bno_data['calibration']
    data = {'heading': heading, 'roll': roll, 'pitch': pitch, 'temp': temp,
            'quatX': x, 'quatY': y, 'quatZ': z, 'quatW': w,
            'calSys': sys, 'calGyro': gyro, 'calAccel': accel, 'calMag': mag }
    return data


async def serial_read():
    data = b''

    wait_bytes = ser.inWaiting()

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


async def websocket_write_loop():
    while True:
        if cfg.sensors.bno055:
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

    def initialize(self, debug=False):
        self.debug = debug
        self.name = 'WebSocketHandler'

    def log(self, text):
        print(self.name + ' ' + text)

    def valid_jasonparse(self, text):
        text = text.replace('\'', '\\"')
        text = text.replace('True', 'true')
        text = text.replace('False', 'false')
        return text

    # websocket abstract methods
    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)
        if self.debug:
            self.log('new connection was opened')
        pass

    def on_close(self):
        self.connections.remove(self)
        if self.debug:
            self.log('connection closed')
        pass

    def on_message(self, message):
        if self.debug:
            self.log('WebSocket message: ' + str(message))
        m = message
        result = 'failed'
        try:
            if isinstance(m, str):
                m = json.loads(message)
            if 'component' in m:
                if m['component'] in components:
                    component = components[m["component"]]
                    result = component.handleMessage(m)
                    if isinstance(result, dict):
                            result = json.dumps(result)
                            result = self.valid_jasonparse(result)
                if m['component'] == 'fpvcar':
                    if 'shutdown' in m:
                        _shutdown = m['shutdown']
                        helper.shutdown(_shutdown)
                        p1.terminate()
                if self.debug:
                    self.log('compent result:' +str(result))
            else:
                if self.debug:
                   self.log('unknown component')
        except Exception as e:
            self.log('failed handling message with :' + str(e))
        try:
            websocket_write(result)
        except Exception as e:
            self.log('failed returning result with :' + str(e))


class WebApplication(tornado.web.Application):
    def __init__(self, components, debug):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'

        handlers = [
            (r'/', HandlerIndexPage, dict(helper=helper)),
            (r'/fpvcar/(.*)', tornado.web.StaticFileHandler, {'path': web_resources}),
            (r'/shutdown', HandlerShutdown),
            (r'/websocket', WebSocketHandler, dict(debug=debug))
        ]

        settings = {
            'autoreload': debug,
            'debug': debug,
            'static_path': web_resources,
            'template_path': 'web_templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class WebServer:
    def __init__(self):
        self.name = 'webserver'

        ser.flushInput()
        cmd = "v\r"
        ser.write(cmd.encode())

        # run info
        for info in helper.infos():
            print(info)

        if cfg.sensors.bno055:
            print('start bno055 read')
            bno_thread = threading.Thread(target=read_bno)
            bno_thread.daemon = True  # Don't let the BNO reading thread block exiting.
            bno_thread.start()

        ws_app = WebApplication(components, cfg.debug)
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(cfg.port)

        print('Start web server at port:' + str(cfg.port))
        IOLoop.current().spawn_callback(websocket_write_loop)
        IOLoop.instance().start()


if __name__ == '__main__':

    running = True
    try:
        # start processes
        p1 = Process(target=WebServer)
        p1.daemon = True
        p1.start()

        print('PID Webserver', p1.pid)

        while running:
            sleep(0.5)

    except KeyboardInterrupt:
        print('ending with keyboard interrupt')
        running = False
        p1.terminate()
    except Exception as e:
        print('error in fpvcar __main__ ' + str(e))

    running = False
    print('[FPVCAR]bye')
    sys.exit()
