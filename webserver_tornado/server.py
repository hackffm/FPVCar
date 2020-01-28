import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from tornado import gen
import serial
import _thread
import pygame
import socket
import json
from components import *
import asyncio
from tornado.websocket import websocket_connect

ser = serial.Serial('/dev/ttyS0', 38400)
print(ser.name)
hostname = socket.gethostname()
print(hostname)
pygame.mixer.init(44100, -16, 1, 1024)

components = {
    "base": Base(ser),
    "sound": Sound(ser),
    "cam": Cam(ser),
    "stats": Stats(ser)
}

def readSerial():
	global data
	try:
		data
	except:
		data = b''
	for i in range(ser.inWaiting()):
		b = ser.read(1)
		if(b != b'\r'): 
			if(b == b'\n'):
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
        print ('from WebSocket: ', message)
        m = json.loads(message)
        component = components[m["component"]]
        component.handleMessage(m)

    def on_close(self):
        self.connections.remove(self)
        print('connection closed')
        pass

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index_neu.html", hostname=hostname)
        
class CssPageHandler(tornado.web.RequestHandler):  
    def get(self):
        self.set_header("Content-Type", 'text/css')
        self.render("style.css", hostname=hostname)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/style.css', CssPageHandler),
            (r'/websocket', WebSocketHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': './root'})
        ]
        settings = {
            'autoreload': True,
            'debug': True,
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)
        self.ws = None
        self.connectToLabyrinth()
        
    @gen.coroutine
    def connectToLabyrinth(self):
        print("trying to connect to labyrinth")
        try:
            self.ws = yield websocket_connect("ws://labyrinth:3000/ws")
        except Exception:
            print("connection error")
        else:
            print("connected")
        self.receiverLoop()

    @gen.coroutine
    def receiverLoop(self):
        while True:
            msg = yield self.ws.read_message()
            print("from labyrinth: " + msg)
            try:
                m = json.loads(msg)
            except Exception:
                print("no json")
            else: 
                component = components[m["component"]]
                print(component)
                component.handleMessage(m)
                if msg is None:
                    print("connection to labyrinth closed")
                    self.ws = None
                    break

if __name__ == '__main__':
    ser.flushInput()
    _thread.start_new_thread(readSerial, ())
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(9090)
    loop = tornado.ioloop.IOLoop.instance()
    serial_loop = tornado.ioloop.PeriodicCallback(readSerial, 30)
    serial_loop.start()    
    loop.start()
