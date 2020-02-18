from . import Thing


class ThingSerial(Thing):

    def __init__(self, name, ser, debug=False):
        super().__init__(name)
        self.ser = ser
        self.debug = debug

    def handleMessage(self, message):
        result = ''

        if self.debug:
            print(self.name + ' recieved ' + str(message))

        self.ser.write(message)

    def serial_read(self):
        data = b''

        wait_bytes = self.ser.inWaiting()

        for i in range(self.ser.inWaiting()):
            b = self.ser.read(1)
            if b != b'\r':
                if b == b'\n':
                    return data
                else:
                    data += b
        return False

    def write(self, command):
        self.ser.write(command.encode())
