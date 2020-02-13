from .rfidthing import RfidThing

class Door(RfidThing):

    def __init__(self, labyrinth, tid, rfid, keyId):
        super().__init__(labyrinth, tid, rfid)
        self.keyId = keyId
        self.serialHandler = labyrinth.get_thing('serh')

    def handleMessage(self, msg, m):
        print("Door: " + msg)
        car = self.labyrinth.get_thing(m["car"])
        if m["action"] == "use":
            print("use")
            key = self.labyrinth.get_thing(self.keyId)
            if car.useItem(key):
                self.serialHandler.handle_message(msg, m)
