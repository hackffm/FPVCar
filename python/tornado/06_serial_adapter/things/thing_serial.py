from .thing import Thing

from .thingy import Thingy

from time import sleep


class ThingSerial(Thing):

    def __init__(self, id, ser, debug=False):
        super().__init__(id)
        self.ser = ser
        self.debug = debug
        self.thingies = []
        self.verified = False

        self.NOT_VERIFIED = 'not verified'

    def handleMessage(self, message):
        result = ''
        if self.debug:
            print(self.name + ' received ' + str(message))
        self.ser.write(message)

    def read(self):
        if not self.verified:
            return self.NOT_VERIFIED
        data = b''

        wait_bytes = self.ser.inWaiting()

        for i in range(wait_bytes):
            b = self.ser.read(1)
            if b != b'\r':
                if b == b'\n':
                    data = str(data.decode())
                    return data
                else:
                    data += b
        return ''

    def thingy_add(self, id):
        if not self.thingy_exists(id):
            _t = Thingy(id)
            self.thingies.append(_t)
            return 'added'
        else:
            return 'thingy already exists'

    def thingy_exists(self, id):
        for ty in self.thingies:
            if ty.id == id:
                return True
        return False

    def verify(self):
        self.verified = False
        if self.update_id():
            if self.debug:
                print('{} was verified'.format(str(self.id)))
            self.verified = True

    def update_id(self):
        data = ''
        try:
            self.ser.write('?\r'.encode())
            sleep(1.0)
            data = b''
            wait_bytes = self.ser.inWaiting()
            if wait_bytes >= 2:
                for i in range(self.ser.inWaiting()):
                    b = self.ser.read(1)
                    if b != b'\r':
                        if b == b'\n':
                            data = str(data.decode())
                        else:
                            data += b
            else:
                data = ''
        except Exception as e:
            if self.debug:
                print('failed writing to serial port of thing ' + str(self.id) + ' with ' + str(e))
                return False
        if not data == '':
            self.id = data
            return True
        else:
            return False

    def write(self, command):
        try:
            command = str(command) + '\r'
            self.ser.write(command.encode())
        except Exception as e:
            if self.debug:
                print('failed writing to serial port of thing ' + str(self.id) + ' with ' + str(e))
