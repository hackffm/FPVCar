import sys
import tornado.web


class HandlerShutdown(tornado.web.RequestHandler):
    def initialize(self):
        self.name = 'shutdown'

    def get(self):
        infos = ['do shutdown']
        self.render("shutdown.html", title="Shutdown", items=infos)
        sys.exit(0)