from . import Component


class Stats(Component):

    def __init__(self, ser, debug):
        name = 'stats'
        super().__init__(name)
        self.debug = debug
        self.ser = ser

    def handleMessage(self, message):
        result = ''

        if self.debug:
            print(self.name + ' recieved ' + message)

        cmd = "V\r"
        self.ser.write(cmd.encode())
        cmd = "v\r"
        self.ser.write(cmd.encode())

        result = 'wrote V and v to serial'
        return result
