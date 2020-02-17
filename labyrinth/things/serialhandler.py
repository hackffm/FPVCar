from labyrinth.things.thing import Thing

class SerialHandler(Thing):

    def handle_message(self, msg, m):
        print("SerialHandler: " + msg)

