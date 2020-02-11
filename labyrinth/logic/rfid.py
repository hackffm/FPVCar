from .thing import Thing

class Rfid(Thing):

    def __init__(self):
        self.things = {}

    def addThing(self, thing):
        self.things[thing.id] = thing

    def handleMessage(self, msg, m):
        print("Rfid: " + msg)
        thing = self.things[m["id"]]
        if thing is not None:
            thing.handleMessage(msg, m)
