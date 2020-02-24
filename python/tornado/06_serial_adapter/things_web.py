import json
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


# resources
config = Config('labyrinth')
config.load()
configuration = config.configuration
cfg = config.cfg()
debug = cfg.debug
helper = Helper(configuration)

serial_handler = SerialHandler(cfg.things_serial)
serial_handler.things_serial_verify()


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
        try:
            m = json.loads(message)
            if 'thing' in m:
                t = m['thing']
                serial_handler.things_serial_write(t['ID'], t['command'])
                return
            if 'thingy' in m:
                t = m['thingy']
                serial_handler.thingy_write(t['ID'], t['command'])
                return
            # should be never here
            self.log('on_message:' + str(m))
        except Exception as e:
            self.log('on_message failed with ' + str(e))
        pass


class WebApplication(tornado.web.Application):
    def __init__(self, port):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'

        handlers = [
            (r'/', HandlerIndexPage, dict(helper=helper)),
            (r'/things', HandlerThingsPage, dict(helper=helper,  port=port, serial_handler=serial_handler)),
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
        port = configuration['labyrinth']['port']
        print('Start things_web http://' + address + ':' + str(port))
        helper.log_add_text('things_web', 'Start things_web at address ' + address + ' port:' + str(port))

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
        print('[things_web]error in __main__ ' + str(e))

    running = False
    print('[things_web]bye')
    sys.exit()
