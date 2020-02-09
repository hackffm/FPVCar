import os
import sys

import tornado.ioloop
import tornado.web

from multiprocessing import Process
from time import sleep
from tornado.ioloop import IOLoop

from components import *
from resources import *
from web_handlers import *

# resources
config = Config()
configuration = config.configuration
helper = Helper(configuration)
cfg = config.cfg()


name = 'labyrinth'

class WebApplication(tornado.web.Application):
    def __init__(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'

        handlers = [
            (r'/', HandlerIndexPage, dict(helper=helper)),
        ]

        settings = {
            'static_path': web_resources,
            'template_path': 'web_templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class WebServer:
    def __init__(self):
        address = '127.0.0.1'
        port = configuration[name]['port']
        helper.log_add_text(name, 'Start ' + name + 'at address ' + address + ' port:' + str(port))
        print('Start ' + name + 'at address ' + address + ' port:' + str(port))
        ws_app = WebApplication()
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(port, address=address)
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
    print('[' + name + ']bye')
    sys.exit()