from .thing import Thing

from .thingy import Thingy


class ThingSerial(Thing):

    def __init__(self, id, ser, debug=False):
        super().__init__(id)
        self.ser = ser
        self.debug = debug
        self.thingies = []

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

    def thingy_add(self, id):
        if not self.thingy_exists(id):
            _t = Thingy(id)
            self.thingies.append(_t)
        else:
            print('thingy already exists')
        return

    def thingy_exists(self, id):
        for ty in self.thingies:
            if ty.id == id:
                return True
        return False

    def write(self, command):
        self.ser.write(command.encode())
