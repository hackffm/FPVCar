import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
from tornado.ioloop import IOLoop, PeriodicCallback
import asyncio
from tornado import gen
from tornado.websocket import websocket_connect

from tornado.options import define, options

define("port", default=3001, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler), (r"/ws", WsHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 5000).start()
        
    def keep_alive(self):
        logging.info("keep alive")
        self.ws.write_message("keep alive from client")
        
    @gen.coroutine
    def connect(self):
        print("trying to connect")
        try:
            self.ws = yield websocket_connect("ws://localhost:3000/ws")
        except Exception:
            print("connection error")
        else:
            print("connected")
            self.run()
     
    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            logging.info(msg)
            if msg is None:
                print("connection closed")
                self.ws = None
                break

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")        
        
class WsHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected.")

    def on_close(self):
        logging.info("A client disconnected")

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