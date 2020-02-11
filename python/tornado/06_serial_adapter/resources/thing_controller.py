import serial
import serial.tools.list_ports

from components import *
from resources import *


class ThingController:

    def __init__(self, debug=False):
        self.debug = debug
        self.things = []
        self.things_find()

    def things_find(self):
        if self.debug:
            print('search used serial ports')
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 0:
            if self.debug:
                print('no used ports found')
        for p in ports:
            if self.debug:
                print('thing is ' + p.description + ' on port ' + p.device)
            ser = serial.Serial(p.device, 38400)
            _t = Thing(p.description, ser)
            self.things.append(_t)
