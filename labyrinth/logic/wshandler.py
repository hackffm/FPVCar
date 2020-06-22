import json
import tornado.websocket

class WsHandler(tornado.websocket.WebSocketHandler):

    labyrinth = None;
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        print("A client connected from " + self.request.remote_ip)
        WsHandler.connections.add(self)

    def on_close(self):
        print("A client disconnected")
        WsHandler.connections.remove(self)

    def on_message(self, msg):
        print("WsHandler: msg: {}".format(msg))
        m = json.loads(msg)
        if 'init' in m:
            car = WsHandler.labyrinth.get_thing(m['tid'])
            car.wshandler = self
        else:
            WsHandler.labyrinth.handle_message(msg, m)
