import os
import sys

import tornado.web
import tornado.httpserver
import tornado.websocket

from multiprocessing import Process
from time import sleep
from tornado.ioloop import IOLoop

from components import *
from resources import *
from web_handlers import *

name = 'Things'
# resources
config = Config(name=name)
configuration = config.configuration
helper = Helper(configuration)
things_controller = ThingController()

cfg = config.cfg()
debug = cfg.debug


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
        self.log('WebSocket message: ' + str(message))
        pass


class WebApplication(tornado.web.Application):
    def __init__(self, port):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'

        handlers = [
            (r'/', HandlerIndexPage, dict(helper=helper)),
            (r'/things', HandlerThingsPage, dict(helper=helper,  port=port, things_controller=things_controller)),
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
    def __init__(self, helper):
        address = helper.interfaces_first()
        port = configuration[name]['port']
        print('Start ' + name + 'at address ' + address + ' port:' + str(port))
        helper.log_add_text(name, 'Start ' + name + 'at address ' + address + ' port:' + str(port))

        ws_app = WebApplication(port)
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(port, address=address)
        IOLoop.instance().start()


if __name__ == '__main__':
    running = True
    try:
        # start processes
        p1 = Process(target=WebServer(helper))
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
        print('['  + name + ']error in __main__ ' + str(e))

    running = False
    print('[' + name + ']bye')
    sys.exit()
