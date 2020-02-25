from labyrinth.things.rfid import Rfid
from labyrinth.things.serialhandler import SerialHandler
from labyrinth.things.keycard import KeyCard
from labyrinth.things.door import Door
from labyrinth.things.car import Car
from labyrinth.things.controller import Controller

class Labyrinth:

    def __init__(self):
        print("Labyrinth")

        self.things = {}
        self.add_thing(Rfid(self, "rfid"))
        serHandler = SerialHandler(self, "serh")
        self.add_thing(serHandler)
        self.add_thing(KeyCard(self, "kc1234", "100101011"))
        self.add_thing(Door(self, "door1234", "111111101", 'kc1234'))
        self.add_thing(Door(self, "door666", "111110001", 'kc1234'))
        self.add_thing(Car(self, "car1"))
        self.add_thing(Car(self, "car2"))
        self.add_thing(Controller(self, "ctrl1"))
        self.add_thing(Controller(self, "ctrl2"))

        rfid = self.things["rfid"]
        rfid.addThing(self.things["kc1234"])
        rfid.addThing(self.things["door1234"])

        self.things["car1"].ctrl = self.things["ctrl1"]
        self.things["car2"].ctrl = self.things["ctrl2"]

        #serHandler.find_my_things()

    def add_thing(self, thing):
        self.things[thing.tid] = thing

    def get_thing(self, tid):
        return self.things[tid]

    def handle_message(self, msg, m):
        self.handle_message(msg, m, None)

    def handle_message(self, msg, m, handler):
        print("labyrinth.handle_message: " + msg)
        # WsHandler.send_car(0, msg)
        thing = self.things[m["thing"]]
        if thing is not None:
            if 'init' in m:
                thing.wshandler = handler
            thing.handleMessage(msg, m)