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
        handlers = [(r"/", IndexPageHandler), 
                    (r"/player.html", PlayerPageHandler), 
                    (r"/playerstyle.css", PlayerCssPageHandler), 
                    (r"/playerscript.js", PlayerScriptPageHandler),
                    (r"/ws", WsHandler),
                    (r'/(.*)', tornado.web.StaticFileHandler, {'path': './root'})]
        #settings = dict(debug=True,)
        settings = { 'template_path': 'templates', 'debug': 'True'}
        tornado.web.Application.__init__(self, handlers, **settings)
        PeriodicCallback(self.keep_alive, 10000).start()

    def keep_alive(self):
        logging.info("keep alive")
        [con.write_message("keep alive from server") for con in WsHandler.connections]  

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", hostname=hostname)

class PlayerPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("player.html", hostname=hostname)
        
class PlayerCssPageHandler(tornado.web.RequestHandler):  
    def get(self):
        self.set_header("Content-Type", 'text/css')
        self.render("playerstyle.css", hostname="schokomobile")
      
class PlayerScriptPageHandler(tornado.web.RequestHandler):  
    def get(self):
        self.set_header("Content-Type", 'text/javascript')
        self.render("playerscript.js", hostname=hostname)
        
class WsHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected." + self.request.remote_ip)
        self.connections.add(self)

    def on_close(self):
        logging.info("A client disconnected")
        self.connections.remove(self)

    def on_message(self, message):
        logging.info("message: {}".format(message))
        [con.write_message(message) for con in self.connections]


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()