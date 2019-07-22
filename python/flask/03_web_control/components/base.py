from . import Component


class Base(Component):
    """docstring for Base."""

    def __init__(self, handler):
        super().__init__('base', handler)

    def do_move(self, command):
        result = 'move base ' + command
        return result
