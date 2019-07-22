import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import serial
import _thread
import pygame
import socket

ser = serial.Serial('/dev/ttyS0', 38400)
print(ser.name)
hostname = socket.gethostname()
print(hostname)
pygame.mixer.init(44100, -16, 1, 1024)

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
		if(message[0] == 'x'):
			print('x')
			pygame.mixer.music.load("sound/chicken.wav")
			#pygame.mixer.music.load("/home/pi/Music/cow.wav")
			pygame.mixer.music.play()
		else:
			ser.write(message.encode());	# received from WebSocket writen to arduino

	def on_close(self):
		self.connections.remove(self)
		print('connection closed')
		pass

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", hostname=hostname)


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
    ser.flushInput()
    _thread.start_new_thread(readSerial, ())
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(9090)
    loop = tornado.ioloop.IOLoop.instance()
    serial_loop = tornado.ioloop.PeriodicCallback(readSerial, 30)
    serial_loop.start()    
    loop.start()
