
class Base(object):
    """docstring for Base."""

    def __init__(self):
        super(Base, self).__init__()
        self.name = 'base'

    def do_move(self, command):
        result = 'move base ' + command
        return result

# -- Helper -----------------------
    def is_base_module(self, module):
        if self.name in module:
            return True
        else:
            return False
