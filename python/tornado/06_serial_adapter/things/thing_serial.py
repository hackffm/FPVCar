from .thing import Thing

from .thingy import Thingy

import string
import random

from time import sleep


class ThingSerial(Thing):

    def __init__(self, id, ser, debug=False):
        super().__init__(id)
        self.ser = ser
        self.debug = debug
        self.thingies = []
        self.verified = False

    def handleMessage(self, message):
        result = ''
        if self.debug:
            print(self.name + ' received ' + str(message))
        self.ser.write(message)

    def read(self):
        if not self.verified:
            return 'not verified'
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
        else:
            print('thingy already exists')
        return

    def thingy_exists(self, id):
        for ty in self.thingies:
            if ty.id == id:
                return True
        return False

    def verify(self):
        self.verified = False
        self.update_id()
        if 'None' not in self.id:
            self.verified = True

    def update_id(self):
        data = ''
        try:
            self.ser.write('?\r'.encode())
            sleep(1)
            data = b''
            for i in range(self.ser.inWaiting()):
                b = self.ser.read(1)
                if b != b'\r':
                    if b == b'\n':
                        data = str(data.decode())
                    else:
                        data += b
        except Exception as e:
            if self.debug:
                print('failed writing to serial port of thing ' +str(self.id) + ' with ' + str(e))
        if not data == '':
            self.id = data
        else:
            self.id = 'None_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    def write(self, command):
        if not self.verified:
            return
        command = str(command) + '\r'
        self.ser.write(command.encode())
