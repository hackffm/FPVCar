from . import Component


class Thing(Component):

    def __init__(self, name, ser, debug=False):
        super().__init__(name)
        self.ser = ser
        self.debug = debug

    def handleMessage(self, message):
        result = ''

        if self.debug:
            print(self.name + ' recieved ' + str(message))

        self.ser.write(message)
