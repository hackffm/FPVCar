import os
import tornado.web
from tornado.ioloop import IOLoop

from web_handlers import *


class WebApplication(tornado.web.Application):
    def __init__(self, components, debug):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'

        handlers = [
            (r'/', HandlerIndexPage),
            (r'/fpvc/api/base', HandlerBase),
            (r'/fpvc/api/component', HandlerComponent, dict(components=components, debug=debug)),
            (r'/fpvc/(.*)', tornado.web.StaticFileHandler, {'path': web_resources}),
            (r'/shutdown', HandlerShutdown)
        ]

        settings = {
            'static_path': web_resources,
            'template_path': 'web_templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class WebServer:
    def __init__(self, components, debug):
        self.name = 'webserver'

        port = 9090
        ws_app = WebApplication(components, debug)
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(port)
        IOLoop.instance().start()

        print('Start web server at port:' + str(port))

