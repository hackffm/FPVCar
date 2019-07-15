
class Component:

    def __init__(self, ser):
        self.ser = ser

    def handleMessage(self, message):
        print(message)

        
class Base(Component):

    def handleMessage(self, message):
        print("handleMessage")