from .handler import WsHandler


class Labyrinth:
    def __init__(self):
        print("Labyrinth")

    def handle_message(self, msg, m):
        print("handle_message: " + msg)
        WsHandler.send_car(0, msg)
