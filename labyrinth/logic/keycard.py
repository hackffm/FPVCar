from .thing import Thing

class KeyCard(Thing):

    def __init__(self, id):
        self.id = id

    def handleMessage(self, msg, m):
        print("KeyCard: " + msg)
