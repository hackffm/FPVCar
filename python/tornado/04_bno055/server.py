import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import serial
import _thread
import json
from components import *

helper = Helper()

# config
baud = 38400
data = b''
debug = True
port = 9090

ser = serial.Serial('/dev/ttyS0', baud)
ip_first = helper.interfaces_first()

# run info
infos = helper.infos_self()
infos.append(port)

components = {
    "sensor": Bno055(debug=debug),
    "stats": Stats(ser, debug=debug)
}


def readSerial():
    global data
    for i in range(ser.inWaiting()):
        b = ser.read(1)
        if b != b'\r':
            if (b == b'\n'):
                print('msg from arduino: ', data)
                websocket_write(data)
                data = b''
            else:
                data += b


def websocket_write(message):
    if type(message) == dict:
        message = json.dumps(message)
        [con.write_message(message) for con in WebSocketHandler.connections]
    else:
        [con.write_message(message.decode("utf-8")) for con in WebSocketHandler.connections]


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        self.connections.add(self)
        print('new connection was opened')
        pass

    def on_message(self, message):
        print('from WebSocket: ', message)
        m = json.loads(message)
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
    _thread.start_new_thread(readSerial, ())
    ws_app = Application(debug=debug)
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(port)
    for info in infos:
        print(info)

    print('start server')
    loop = tornado.ioloop.IOLoop.instance()
    serial_loop = tornado.ioloop.PeriodicCallback(readSerial, 30)
    serial_loop.start()
    loop.start()
