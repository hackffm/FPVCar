from . import Component


class Stats(Component):

    def __init__(self, ser, debug):
        name = 'stats'
        super().__init__(name)
        self.debug = debug
        self.name = name
        self.ser = ser

    def handleMessage(self, message):
        result = {}

        if self.debug:
            print(self.name + ' recieved ' + message["action"])

        if not self.is_valid(message):
            result[self.name] = self.failed
            return result

        cmd = "V\r"
        self.ser.write(cmd.encode())
        cmd = "v\r"
        self.ser.write(cmd.encode())
