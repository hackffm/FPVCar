import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import asyncio
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import define, options
import socket

define("port", default=3000, help="run on the given port", type=int)

hostname = socket.gethostname()
print(hostname)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexPageHandler), (r"/player.html", PlayerPageHandler), (r"/ws", WsHandler)]
        #settings = dict(debug=True,)
        settings = { 'template_path': 'templates', 'debug': 'True'}
        tornado.web.Application.__init__(self, handlers, **settings)
        PeriodicCallback(self.keep_alive, 6000).start()

    def keep_alive(self):
        logging.info("keep alive")
        [con.write_message("keep alive from server") for con in WsHandler.connections]  

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", hostname=hostname)

class PlayerPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("player.html", hostname=hostname)
        
class WsHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected.")
        self.connections.add(self)

    def on_close(self):
        logging.info("A client disconnected")
        self.connections.remove(self)

    def on_message(self, message):
        logging.info("message: {}".format(message))


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()