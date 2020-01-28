import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import asyncio
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler), (r"/ws", WsHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)
        PeriodicCallback(self.keep_alive, 6000).start()

    def keep_alive(self):
        logging.info("keep alive")
        [con.write_message("keep alive from server") for con in WsHandler.connections]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")        
        
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
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()