from random import random
import serial
import serial.tools.list_ports

from things import *


class SerialHandler:
    def __init__(self, things_serial, debug=False):
        self.debug = debug
        self.things_serial = []
        if things_serial:
            self.things_add(things_serial)

    def things_add(self, things_serial):
        for ts in things_serial:
            self.things_serial_add(ts['ID'], ts['port'], self.debug)
        print('add thingies')
        for ts in things_serial:
            for t in ts['thingies']:
                self.thingy_add(ts['ID'], t['ID'])

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

    def things_serial_read(self, id):
        result = ''
        if self.debug:
            print('read from {}'.format(id))
        for ts in self.things_serial:
            for ty in ts.thingies:
                if ty.id == id:
                    result = ts.read()
        return result

    def things_serial_verify(self):
        for ts in self.things_serial:
            ts.verify()

    def things_serial_write(self, id,  command):
        if self.debug:
            print('Write to {} command {}'.format(id, command))
        for thing in self.things_serial:
            if thing.id == id:
                thing.write(command)

    def thingies(self):
        _thingies = []
        for ts in self.things_serial:
            for ty in ts.thingies:
                _thingies.append(ty.id)
        return _thingies

    def thingy_add(self, id_ts, id_thingy):
        for ts in self.things_serial:
            if ts.id == id_ts:
                result = ts.thingy_add(id_thingy)
                return result
        return 'thing serial not found'

    def thingy_read(self, id):
        for ts in self.things_serial:
            for thingy in ts.thingies:
                if thingy.id == id:
                    result = ts.read()
                    return result
        return 'Thingy not found'

    def thingy_write(self, id, command):
        for ts in self.things_serial:
            for thingy in ts.thingies:
                if thingy.id == id:
                    self.things_serial_write(ts.id,  str(command))
                    return 'Done'
        return 'Thingy not found'
