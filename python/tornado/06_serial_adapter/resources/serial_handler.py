import serial
import serial.tools.list_ports

from things import *


class SerialHandler:
    def __init__(self, debug=False):
        self.debug = debug
        self.things_serial = []
        self.things_serial_find()

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
                print('thing is ' + p.description + ' on port ' + p.device)
            ser = serial.Serial(p.device, 38400)
            _t = ThingSerial(p.description, ser, self.debug)
            self.things_serial.append(_t)

    def things_serial_write(self, id,  command):
        if self.debug:
            print('id {} write {}'.format(str(t['ID']), str(t['command'])))
        for thing in self.things_serial:
            if thing.id == id:
                thing.write(command)

    def write(self, id, command):
        self.things_serial_write(str(id),  str(command))
