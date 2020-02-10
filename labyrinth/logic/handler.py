import json
import tornado.websocket

class WsHandler(tornado.websocket.WebSocketHandler):
    connections = set()
    car = [None] * 2
    controller = [None] * 2
    labyrinth = None;

    @staticmethod
    def send_car(nbr, msg):
        if WsHandler.controller[nbr] is not None:
            WsHandler.controller[nbr].write_message(msg)

    @staticmethod
    def send_controller(nbr, msg):
        if WsHandler.car[nbr] is not None:
            WsHandler.car[nbr].write_message(msg)

    def check_origin(self, origin):
        return True

    def open(self):
        print("A client connected." + self.request.remote_ip)
        WsHandler.connections.add(self)

    def on_close(self):
        print("A client disconnected")
        WsHandler.connections.remove(self)

    def on_message(self, msg):
        print("msg: {}".format(msg))
        m = json.loads(msg)
        if m["component"] == 'self':
            print("client is called "+m["name"])
            if m["type"] == 'player':
                WsHandler.car[m["nbr"]] = self
            elif m["type"] == 'controller':
                WsHandler.controller[m["nbr"]] = self
        else:
            if m["entity"] == 'car':
                WsHandler.car[m["nbr"]].write_message(msg)
            elif m["entity"] == 'controller':
                WsHandler.controller[m["nbr"]].write_message(msg)
            elif m["entity"] == 'labyrinth':
                WsHandler.labyrinth.handle_message(msg, m)
            else:
                [con.write_message(msg) for con in WsHandler.connections]