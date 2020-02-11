from .thing import Thing

class Car(Thing):

    def __init__(self, id):
        self.id = id

    def handleMessage(self, msg, m):
        print("Car: " + msg)
