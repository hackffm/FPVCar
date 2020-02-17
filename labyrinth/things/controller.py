from labyrinth.things.thing import Thing

class Controller(Thing):

    def __init__(self, labyrinth, tid):
        super().__init__(labyrinth, tid)
        self.wshandler = None

    def handleMessage(self, msg, m):
        if msg is not None:
            print("Controller: " + msg)
            self.wshandler.write_message(msg)
