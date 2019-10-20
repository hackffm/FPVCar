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
port = 9090

ser = serial.Serial('/dev/ttyS0', baud)
ip_first = helper.interfaces_first()

# run info
infos = helper.infos_self()
infos.append(port)

components = {
    "sensor": Bno055(),
    "stats": Stats(ser, True)
}


def readSerial():
    global data
    if not data:
        data = b''
    for i in range(ser.inWaiting()):
        b = ser.read(1)
        if b != b'\r':
            if (b == b'\n'):
                print('msg from arduino: ', data)
                [con.write_message(data.decode("utf-8")) for con in WebSocketHandler.connections]
                data = b''
            else:
                data += b


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
        component.handleMessage(m)

    def on_close(self):
        self.connections.remove(self)
        print('connection closed')
        pass


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", ip_first=ip_first)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': './root'})
        ]

        settings = {
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(port)
    for info in infos:
        print(info)

    loop = tornado.ioloop.IOLoop.instance()
    loop.start()
