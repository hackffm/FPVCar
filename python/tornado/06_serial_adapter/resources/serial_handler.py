from random import random
import serial
import serial.tools.list_ports

from things import *


class SerialHandler:
    def __init__(self, debug=False):
        self.debug = debug
        self.things_serial = []

    def things_serial_exists(self, id):
        for t in self.things_serial:
            if t.id == id:
                return True
        return False

    def things_serial_add(self, id, port, debug):
            ser = random()
            try:
                ser = serial.Serial(port, 38400)
            except Exception:
                print('failed accessing ' + str(port))
            _t = ThingSerial(id, ser, debug)
            self.things_serial.append(_t)

    def things_serial_find(self):
        if self.debug:
            print('search used serial ports')
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 0:
            if self.debug:
                print('no used ports found')
        self.things_serial = []
        for p in ports:
            if self.debug:
                print('found thing ' + p.description + ' on port ' + p.device)
            self.things_serial_add(p.description, p.device, self.debug)

    def things_serial_write(self, id,  command):
        if self.debug:
            print('id {} write {}'.format(str(t['ID']), str(t['command'])))
        for thing in self.things_serial:
            if thing.id == id:
                thing.write(command)

    def thingy_add(self, id_ts, id_thingy):
        for ts in self.things_serial:
            if ts.id == id_ts:
                ts.thingy_add(id_thingy)
        return

    def thingy_exists(self, id):
        for ts in self.things_serial:
            if ts.thingy_exists(id):
                return True
        return False

    def write(self, id, command):
        self.things_serial_write(str(id),  str(command))
