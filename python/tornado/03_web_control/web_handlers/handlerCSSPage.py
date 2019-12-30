import socket
import tornado.web


class CssPageHandler(tornado.web.RequestHandler):
    def get(self):
        hostname = str(socket.gethostname())
        self.set_header("Content-Type", 'text/css')
        self.render("style.css", hostname=hostname)
