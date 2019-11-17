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

# config
baud = 38400
data_sensor = {}
data_serial = b''
debug = True
port = 9090
sensors = {}

# run info
helper = Helper()
infos = helper.infos_self()
infos.append(port)
#
ip_first = helper.interfaces_first()
sensor = Bno055()
ser = serial.Serial('/dev/ttyS0', baud)


# load components statically
components = {
    "base": Base(ser, debug=debug),
    "sensor": Bno055(debug=debug),
    "stats": Stats(ser, debug=debug)
}

async def read_sensor():
    data_sensor = sensor.handleMessage({'sensor': 'all'})
    return data_sensor


async def serial_read():
    data = b''
    wait_bytes = ser.inWaiting();

    if not wait_bytes:
        return False

    for i in range(wait_bytes):
        b = ser.read(1)
        if b != b'\r':
            if b == b'\n':
                return data
            else:
                data += b


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

        port = 9090
        ws_app = WebApplication(components, debug)
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(port)
        print('Start web server at port:' + str(port))
        IOLoop.instance().start()

        print('start async callbacks')
        IOLoop.current().spawn_callback(websocket_loop)
        IOLoop.instance().start()