from .rfidthing import RfidThing

class KeyCard(RfidThing):

    def handleMessage(self, msg, m):
        print("KeyCard: " + self.rfid + "  " + msg)
        car = self.labyrinth.get_thing(m["car"])
        if m["action"] == "add":
            print("add")
            car.addItem(self)
        elif m["action"] == "rem":
            print("rem")
            car.removeItem(self)

