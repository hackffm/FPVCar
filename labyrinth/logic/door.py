from .thing import Thing

class Door(Thing):

    def __init__(self, id):
        self.id = id

    def handleMessage(self, msg, m):
        print("Door: " + msg)
