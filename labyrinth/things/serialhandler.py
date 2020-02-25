from labyrinth.things.thing import Thing
import serial
import serial.tools.list_ports
from time import sleep
from tornado import gen

class SerialHandler(Thing):

    def __init__(self, labyrinth, tid):
        super().__init__(labyrinth, tid)
        self.serials = []

    def handle_message(self, msg, m):
        print("SerialHandler: " + msg)

    def write(self, ser, command):
        command = str(command) + '\r'
        ser.write(command.encode())

    def serial_read(self, ser):
        data = b''
        wait_bytes = ser.inWaiting()
        if wait_bytes == 0:
            return False
        print(str(wait_bytes) + ' bytes waiting in serial port')
        for i in range(ser.inWaiting()):
            b = ser.read(1)
            if b != b'\r':
                if b == b'\n':
                    return data
                else:
                    data += b
        return False

    def find_my_things(self):
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 0:
            print('no used ports found')
        for p in ports:
            print('write to ' + p.description + ' on port ' + p.device)
            ser = serial.Serial(p.device, 38400, )
            self.serials.append(ser)
            self.write(ser, '?')
            sleep(0.2)
            sr = self.serial_read(ser)
            if sr is False:
                break
            result = str(sr.decode())
            print('Serial result was ' + result)
            tokens = result.split(" ")
            tids = tokens[1].split(",")
            for tid in tids:
                thing = self.labyrinth.get_thing(tid)
                thing.ser = ser
        self.loop()

    @gen.coroutine
    def loop(self):
        while True:
            yield gen.sleep(1)
            data = b''
            for p in self.serials:
                data = self.serial_read(p)
                if data is not False:
                    print(data)
