from . import Component


class Base(Component):
    """docstring for Base."""

    def __init__(self, handler):
        super().__init__('base', handler)

    def handle_message(self, message):
        result = 'no usefull command found'
        if "right" in message:
            result = self.move_right(message)

        return result

    def move_right(self, message):
        cmd = str(message["right"])
        result = self.message_handler.send('move base right :' + cmd)
        return result

    def do_move(self, command):
        result = 'move base ' + command
        return result
