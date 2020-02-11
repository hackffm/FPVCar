from .thing import Thing

class Controller(Thing):

    def __init__(self, id):
        self.id = id

    def handleMessage(self, msg, m):
        print("Controller: " + msg)
