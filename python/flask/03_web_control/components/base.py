from components import Component


class Base(Component):
    """docstring for Base."""

    def __init__(self):
        super().__init__('base')

    def do_move(self, command):
        result = 'move base ' + command
        return result
