from .handler import WsHandler
from .rfid import Rfid
from .keycard import KeyCard
from .door import Door
from .car import Car
from .controller import Controller

class Labyrinth:

    things = {
        "rfid": Rfid(),
        "kc1234": KeyCard("kc1234"),
        "door1234": Door("door1234"),
        "car1": Car("car1"),
        "car2": Car("car2"),
        "ctrl1": Controller("ctrl1"),
        "ctrl2": Controller("ctrl2")
    }
    rfid = things["rfid"]
    rfid.addThing(things["kc1234"])
    rfid.addThing(things["door1234"])

    def __init__(self):
        print("Labyrinth")

    def handle_message(self, msg, m):
        print("labyrinth.handle_message: " + msg)
        #WsHandler.send_car(0, msg)
        thing = Labyrinth.things[m["thing"]]
        if thing is not None:
            thing.handleMessage(msg, m)


