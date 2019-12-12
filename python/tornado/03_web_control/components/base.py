from . import Component


class Base(Component):
    """control movements of base"""

    def __init__(self, ser, debug=False):
        name = 'base'
        super().__init__(name)
        self.debug = debug
        self.ser = ser

    def handleMessage(self, message):
        result = 'unknown command'

        if self.debug:
            print(self.name + ' recieved ' + str(message))

        if "right" in message:
            result = self.move_right(message)
        return result

    def move_right(self, message):
        cmd = str(message["right"])
        result = self.ser.send('move base right :' + cmd)
        return result

    def do_move(self, command):
        result = 'move base ' + command
        return result
