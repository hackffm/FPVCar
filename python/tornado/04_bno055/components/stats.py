from . import Component


class Stats(Component):

    def __init__(self, ser, debug):
        self.debug= debug
        self.ser = ser

    def handleMessage(self, message):
        if self.debug:
            print("Stats.handleMessage")
        cmd = "V\r"
        if self.debug:
            print("fetch: " + cmd)
        self.ser.write(cmd.encode())
        cmd = "v\r"
        if self.debug:
            print("fetch: " + cmd)
        self.ser.write(cmd.encode())