import logging
import socket
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback
from tornado.options import define, options
from tornado import gen
import toml
from logic import WsHandler
from logic import Labyrinth

define("port", default=3000, help="run on the given port", type=int)

config = toml.load('config_strange.toml')
print(config)
hostname = socket.gethostname()
print(hostname)

labyrinth = Labyrinth()
WsHandler.labyrinth = labyrinth

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", IndexPageHandler), 
                    (r"/player.html", PlayerPageHandler), 
                    (r"/playerstyle.css", PlayerCssPageHandler),
                    (r"/ws", WsHandler),
                    (r'/(.*)', tornado.web.StaticFileHandler, {'path': './root'})]
        #settings = dict(debug=True,)
        settings = {'template_path': 'templates', 'debug': 'True'}
        tornado.web.Application.__init__(self, handlers, **settings)
        PeriodicCallback(self.keep_alive, 10000).start()
        serialHandler = labyrinth.get_thing('serh')
        serialHandler.find_my_things()

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

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
