from . import Component


class Base(Component):
    """control movements of base"""

    def __init__(self, ser, debug):
        super().__init__('base')
        self.debug = debug
        self.ser = ser

    def handle_message(self, message):
        result = 'no usefull command found'
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
