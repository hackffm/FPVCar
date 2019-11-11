import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import serial
import json

from tornado import gen
from tornado.ioloop import IOLoop

from components import *

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
    "sensor": Bno055(),
    "stats": Stats(ser, debug=debug)
}


async def read_sensor():
    global data_sensor
    data_sensor = sensor.handleMessage({'sensor': 'all'})
    return data_sensor


async def serial_read():
    data = b''
    for i in range(ser.inWaiting()):
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

    def open(self):
        self.connections.add(self)
        print('new connection was opened')
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

    def on_close(self):
        self.connections.remove(self)
        print('connection closed')
        pass


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

    ws_app = Application(debug=debug)
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(port)

    for info in infos:
        print(info)

    print('start server')
    IOLoop.current().spawn_callback(websocket_loop)
    IOLoop.instance().start()
